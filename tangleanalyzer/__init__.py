
# Make some imports accessible from the top level of the package.
# Note that order is important, to prevent circular imports.
from .filter import *
from .importer import *


# MILESTONES_USING_TIMESTAMP_ONLY: set([str]) = set(
#     ['6000', '13157', '18675', '61491', '150354', '216223', '242662', '337541'])
# """
# For the transactions with milestones in MILESTONES_USING_TIMESTAMP_ONLY, the timestamp is used directly.
# For other transactions, the attachmentTimestamp will be used if it is not zero, else timestamp is used.
# """
