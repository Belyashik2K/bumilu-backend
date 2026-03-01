import warnings

from fastapi.exceptions import FastAPIDeprecationWarning

warnings.filterwarnings("ignore", category=FastAPIDeprecationWarning)
