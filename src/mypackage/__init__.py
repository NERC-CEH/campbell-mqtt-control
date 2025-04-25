import autosemver

try:
    __version__ = autosemver.packaging.get_current_version(project_name="mypackage")
except Exception:
    __version__ = "0.0.0"
