# Fast api

This project is a little and simple project with python and **Fast API**.

## Getting started

You need python _3.14_ and poetry. Once time you have this software installed
you can run the environment so easy

```zsh
    poetry install
    poetry shell
```

If you are inside of the virtual environment you can run in your local the project,
by default we are using the port 8000

```zsh
    uvicorn main:app --reload
```

The framework load by default the UI of **Open API** then we can access to that
documentation in port 8000 and path **/docs**.

Also the project has a makefile archive where you can do the more important
actions directly.
