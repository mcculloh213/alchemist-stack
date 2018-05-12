# alchemist-stack
**Package Author**: H.D. 'Chip' McCullough IV

**Last Updated**: April 23rd, 2018

**Description**:\
A Flexible Model-Repository-Database stack for use with SQL Alchemy

## Overview
Alchemist Stack is intended to be a thread-safe, multi-session/multi-connection 

## Motivation

The motivation for this package started partly out of API documentation procrastination, and partly from noticing that 
the API I was documenting created a single connection on startup that persisted though the life of the API. In theory, 
(kind of) works for Development environments, and may even (kind of) work in Production environments under light load 
(the operating words being "light load"). In practice, it doesn't make sense for the database to create a connection 
pool, have the server spawn N worker threads, then take a single connection from the connection pool, and use that 
single connection for all N worker threads. Under heavy load, that single connection is a bottleneck that would have to 
serve all requests coming in.

Thus, the problem is how do we create a multi-connection environment to alleviate the bottleneck single-connection 
environment that is already in place? Astoundingly, SQL Alchemy already has that solved, with their Session API 
(/sarcasm). Using the Session API, Alchemist Stack provides a base Repository object, RepositoryBase, that (at the time 
of writing) abstracts the Session API to the four CRUD operations (Create, Read, Update, and Delete). While this does 
leave the developer with a quite a bit to finish implementing, it provides a quality scaffolding to get ~80% (don't 
fact check me on that number) of all web app projects up and running as quickly as possible.

Now, this leaves one last issue: SQL Alchemy's Session API isn't thread safe. This is solved in two ways:
  1. The RepositoryBase contains an abstract class method, `instance`, which must be implemented (or not) by the 
  child class.
  2. The RepositoryBase contains a function `_create_thread_safe_session()`, which creates a thread-local Session, 
  which any thread can utilize through the life cycle of that Session.

While Alchemist Stack was implemented with the 

### The RepositoryBase `instance` Method

The `instance` method, which takes in a Context object, returns a new instance of the implemented repository. That 
instance holds the  Context used to connect to and query the database. 

In the context of an API call, it is safe to create a new instance at the beginning of the request, run a CRUD 
operation, create and use a raw Session, do what you need, commit everything to the database, handle any errors 
(because no software is perfect), then dispose of the instance at the end of the request.

Implementation of the `instance` method is incredibly straightforward, whether you intend to use it, or not. To 
implement it for use,

```python
T = TypeVar('T', bound='your class here')
    @classmethod
    def instance(cls, context: Context) -> T:
        return cls(context=context)
```
And you're done! Likewise, to implement it for !use,
```python
    @classmethod
    def instance(cls, context: Context) -> NoReturn:
        pass
```
Of course, I would recommend implementing the `instance` method, if not for full flexibility, then for completion, 
but I can't tell you how to code.

### The RepositoryBase `_create_thread_safe_session()` Function

Sometimes, just managing a single instance of a repository and Session isn't enough. Depending on how objects in an 
application interact, it may be more prudent to give multiple repositories access to the same Session, which is where 
SQL Alchemy's `scoped_session(...)` and the RepositoryBase's `_create_thread_safe_session()` come in. Creating a scoped 
Session creates a global Session object than any thread has access to.