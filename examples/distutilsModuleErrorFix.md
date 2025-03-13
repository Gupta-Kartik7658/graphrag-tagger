# Fix for ModuleNotFoundError: No module named 'distutils' in Python 3.12

## Issue
When using `ktrain` with Python 3.12, you may encounter the following error:

```
ModuleNotFoundError: No module named 'distutils'
```

This occurs because `distutils` was removed from the standard library in Python 3.12. `ktrain` still attempts to import it, causing the error.

---

## Solution
### 1. Install `setuptools` (Recommended Fix)
Run the following command to install `setuptools`, which includes `distutils`:

```bash
pip install setuptools
```

Then, restart your Python environment and try running your script again.

---

### 2. Manually Patch `ktrain`
If the issue persists, you can manually modify `ktrain` to avoid the `distutils` import error.

#### Steps:
1. **Locate the `ktrain` package directory:**
   
   Navigate to:
   1. In case of Local installation
   ```
   c:\Users\hp\AppData\Local\Programs\Python\Python312\Lib\site-packages\ktrain\imports.py
   ```
   2. In case of Virtual Environment
   ```
   .\<Your-Virtual-Environment-Name>\Lib\site-packages\ktrain\imports.py  
   ```


2. **Edit the file:**
   Open `imports.py` in a text editor and find this line:
   ```python
   from distutils.util import strtobool
   ```
   
   Replace it with:
   ```python
   from setuptools._distutils.util import strtobool
   ```

3. **Save and restart Python**, then try running your script again.

---

### 3. Use an Older Python Version (Alternative Fix)
If neither of the above solutions works, consider using Python 3.10 or 3.11, which still include `distutils`.

#### Install an older Python version:
- **For `pyenv` users:**
  ```bash
  pyenv install 3.10.12
  pyenv global 3.10.12
  ```

- **For Anaconda users:**
  ```bash
  conda create -n py310_env python=3.10
  conda activate py310_env
  pip install graphrag_tagger ktrain
  ```

Then run your script inside this environment.

---

## Conclusion
If you're using Python 3.12, the best approach is to install `setuptools`. If that doesn't work, manually editing `ktrain` or switching to an older Python version should resolve the issue. If `ktrain` is updated in the future, this issue may be fixed officially.

For more details, check the [`ktrain` GitHub repository](https://github.com/amaiya/ktrain).