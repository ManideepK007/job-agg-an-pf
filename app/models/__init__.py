# This tells Python that 'models' is a package.
# We don't define 'db' here to avoid crashes.

from app.models.user import User
from app.models.profile import Profile
from app.models.job import Job