from zmq.asyncio import Context
import zmq
import asyncio
import concurrent.futures
import functools
import logging
import queue
import random
import signal
import string
import sys
import threading
import time
import uuid
import attr
import iota
from ..common.const import ZMQ_TRYTES_TOPIC_OFFSET

__all__ = [
    'zmq_init',
]


@attr.s
class PubSubMessage:
    instance_name = attr.ib()
    message_id = attr.ib(repr=False)
    content = attr.ib(repr=False)
    hostname = attr.ib(repr=False, init=False)
    restarted = attr.ib(repr=False, default=False)
    saved = attr.ib(repr=False, default=False)
    acked = attr.ib(repr=False, default=False)
    extended_cnt = attr.ib(repr=False, default=0)

    def __attrs_post_init__(self):
        self.hostname = f"{self.instance_name}.tangle.analyzer.net"


class RestartFailed(Exception):
    pass


class ZmqSub():
    """
    Zmq Subscriber for transactions.


    Attributes
    ----------
    url : str
        The url to subscribe.
    topic : str
        The topic to subscribe.

    filterlist : list
        The filter list for new coming transactions.

    Methods
    -------
    run()
        Start to run the zmq subscriber and receive new coming transactions.
    """

    def __init__(self, url='tcp://zmq.iota.org:5556', topic='trytes', filterlist=[]) -> None:
        self.threads = set()
        self.url = url
        self.topic = topic
        self.filterlist = filterlist

    async def push_zmq_msg(self, queue) -> None:
        choices = string.ascii_lowercase + string.digits
        curr_thread = threading.current_thread()
        self.threads.add(curr_thread.ident)
        logging.debug("Starting push_zmq_msg")
        ctx = Context.instance()
        s = ctx.socket(zmq.SUB)
        s.connect(self.url)
        s.subscribe(self.topic)
        while True:
            content = await s.recv_multipart()
            msg_id = str(uuid.uuid4())
            host_id = "".join(random.choices(choices, k=4))
            instance_name = f"ta-{host_id}"
            msg = PubSubMessage(message_id=msg_id,
                                instance_name=instance_name, content=content)
            # publish an item
            queue.put(msg)
            logging.info(f"Received {content[0][:20]}...")
        s.close()

    async def save(self, msg) -> None:
        """Save message to a database.

        Parameters
        ----------
        msg : PubSubMessage
            Consumed event message to be saved.
        """
        trytes_hash = (msg.content[0][ZMQ_TRYTES_TOPIC_OFFSET:],)
        logging.info(f"Start filtering...")
        for f in self.filterlist:
            trytes_hash = tuple(filter(f, trytes_hash))
        if trytes_hash:
            logging.info(f"Saved {trytes_hash[0][:20]}... into database")
        # TODO: save the filtered trytes to database
        msg.save = True

    async def cleanup(self, msg, event) -> None:
        """Cleanup tasks related to completing work on a message.

        Parameters
        ----------
        msg : PubSubMessage
            Consumed event message that is done being processed.
        """
        await event.wait()
        msg.acked = True
        logging.debug(f"Done. Acked {msg}")

    def handle_results(self, results, msg) -> None:
        """Handle exception results for a given message.

        Parameters
        ----------
        results :
            Futures are gathered in asyncio.

        msg : PubSubMessage
            The event message to be handled.
        """
        for result in results:
            if isinstance(result, RestartFailed):
                logging.error(
                    f"Retrying for failure to restart: {msg.hostname}")
            elif isinstance(result, Exception):
                logging.error(f"Handling general error: {result}")

    async def extend(self, msg, event):
        while not event.is_set():

            msg.extended_cnt += 1
            logging.debug(f"Extended deadline by 3 seconds for {msg}")

            # want to sleep for less than the deadline amount
            await asyncio.sleep(2)

    async def handle_message(self, msg) -> None:
        """Kick off tasks for a given message.

        Parameters
        ----------
        msg : PubSubMessage
            consumed message to process.
        """
        event = asyncio.Event()
        asyncio.create_task(self.extend(msg, event))
        asyncio.create_task(self.cleanup(msg, event))

        results = await asyncio.gather(
            self.save(msg), return_exceptions=True
        )

        self.handle_results(results, msg)
        event.set()

    def consume_sync(self, queue, loop) -> None:
        while True:
            msg = queue.get()
            logging.debug(f"Consumed {msg}")
            asyncio.run_coroutine_threadsafe(self.handle_message(msg), loop)

    async def consume(self, executor, queue) -> None:
        logging.debug("Starting consumer")
        loop = asyncio.get_running_loop()
        asyncio.ensure_future(
            loop.run_in_executor(executor, self.consume_sync, queue, loop), loop=loop
        )

    def handle_exception(self, executor, loop, context) -> None:
        # context["message"] will always be there; but context["exception"] may not
        msg = context.get("exception", context["message"])
        logging.error(f"Caught exception: {msg}")
        logging.debug("Shutting down...")
        asyncio.create_task(self.shutdown(loop, executor))

    async def shutdown(self, loop, executor, signal=None) -> None:
        """Cleanup tasks tied to the service's shutdown."""
        if signal:
            logging.info(f"Received exit signal {signal.name}...")
        logging.info("Closing database connections")
        tasks = [t for t in asyncio.all_tasks() if t is not
                 asyncio.current_task()]

        [task.cancel() for task in tasks]

        logging.info(f"Cancelling {len(tasks)} tasks")
        await asyncio.gather(*tasks, return_exceptions=True)

        logging.info("Shutting down ThreadPoolExecutor")
        executor.shutdown(wait=False)

        logging.info(
            f"Releasing {len(executor._threads)} threads from executor")
        for thread in executor._threads:
            try:
                thread._tstate_lock.release()
            except Exception:
                pass

        logging.info(f"Flushing metrics")
        loop.stop()

    def run(self) -> None:
        """Start to run the zmq subscriber and receive new coming transactions."""
        executor = concurrent.futures.ThreadPoolExecutor()
        loop = asyncio.get_event_loop()
        loop.slow_callback_duration = 2.5  # in seconds
        signals = (signal.SIGHUP, signal.SIGTERM,
                   signal.SIGINT, signal.SIGQUIT)
        for s in signals:
            loop.add_signal_handler(
                s, lambda s=s: asyncio.create_task(self.shutdown(loop, executor, signal=s)))
        handle_exc_func = functools.partial(self.handle_exception, executor)
        loop.set_exception_handler(handle_exc_func)
        q = queue.Queue()

        try:
            loop.create_task(self.consume(executor, q))
            loop.create_task(self.push_zmq_msg(q))
            loop.run_forever()
        finally:
            loop.close()
            logging.info("Successfully shutdown. Good bye~")
