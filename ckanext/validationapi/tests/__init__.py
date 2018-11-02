import warnings
from sqlalchemy import exc as sa_exc

warnings.filterwarnings("ignore", category=sa_exc.SAWarning)