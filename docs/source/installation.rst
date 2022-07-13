Installation
============

sGameSolver can be installed using pip.

.. code-block:: console

    pip install sgamesolver

If you are using MacOS or a linux distribution, please check the 
according section under "Cython" below.

Installation with Anaconda
--------------------------

While sGameSolver works fine with the official Python distribution from `python.org`,
we strongly recommend using `Anaconda <https://www.anaconda.com/>`_ for numerical computations
- the speedup provided by Anaconda was sizeable on our systems when using sGameSolver.
If you *do* use Anaconda, make sure to install
:py:mod:`numpy`, :py:mod:`scipy`, :py:mod:`pandas`, :py:mod:`matplotlib` and :py:mod:`cython`
before installing sGameSolver.
Otherwise, these dependencies will be installed by pip
(rather than conda), which should be avoided.
The sequence should thus be

.. code-block:: console

    conda activate my_env
    conda install numpy scipy pandas matplotlib cython
    pip install sgamesolver


Cython
------

The performance-critical routines that evaluate the homotopy function :math:`H`
and its Jacobian :math:`J` are written in Cython. Parts of sGameSolver may 
thus need to be compiled during installation. The following should let you
know if that applies for your situation, and if yes, how 
to prepare your system:

Windows:
********
- We provide wheels for Python versions 3.6--3.10 via PyPI. 
  Wheels are pre-built, so usually **no steps** from your side necessary when 
  installing via pip. 
- Should you want or have to compile anyway, first identify the compiler
  required for your version of Python. 
  Activate your virtual environment and run
  ``python`` in a terminal; you should see a line like

  .. code-block:: console

      Python 3.XXX ... [MSC v.1916 64 bit (AMD64)]
      >>>

  If the number is :code:`MSC v. 1916`, you need to 
  `download <https://visualstudio.microsoft.com/de/vs/older-downloads/>`_ 
  and install Microsoft build tools 2017, if it is :code:`1900`, you'll need 2015.
  When installing, make sure to check "Windows 10 SDK" as well. 
  Once that is done, you can install sGameSolver e.g. via pip.

Linux
*****
- As of now, no wheels yet (but we hope to provide them soon).
- Before installing, just install the compiler gcc. 
- When using Anaconda, Miniconda, or some other derivative, you will have to
  additionally install the package :py:mod:`gxx_linux-64`.
  Otherwise, the installation steps are the same as under Windows.

  .. code-block:: console

      conda activate my_env
      conda install numpy scipy pandas matplotlib cython gxx_linux-64
      pip install sgamesolver

MacOS
*****

- Unfortunately, we have neither experience nor an opportunity to test this setup.
- Your best bet will be to find a guide on how to compile cython modules
  on MacOS, follow instructions and then install sGameSolver as above.
- If you are having trouble relating to OpenMP support, check below
  how to install without.
- If all else fails, you can install without Cython altogether (see below).

Installing without OpenMP
*************************

- OpenMP is a standard for parallel computing; parts of 
  sGameSolver's Cython code make use of it.
- Most compilers (especially linux' gcc, MSVC on windows) support it.
- However, if you have a different setup and experience any related problems 
  during installation, you can disable it by installing via:

  .. code-block:: console

      pip install sgamesolver --install-option="--no-openmp"


Installing without Cython
*************************

- If all else fails, you can install sGameSolver without Cython support --
  in that case, it will fall back to a numpy implementation of the respective
  functions, which will be considerably slower however.
- To do so, make sure :py:mod:`numpy`, :py:mod:`scipy`, :py:mod:`pandas`
  and :py:mod:`matplotlib` are installed. Then run:
  
  .. code-block:: console

      pip install sgamesolver --install-option="--no-cython" --no-deps
