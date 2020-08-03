# AxantAddressBook
A simple local address book built with TurboGears2.
One can create his/her own account and, once logged in, can add and see his/her own contacts.

## Setup and Run
1. Clone this repository in a folder of your choice
2. Setup and start a virtualenv: `$ python3 -m venv myvenv`  ~> `source myenv/bin/activate`
3. Install the toolbox of TurboGears2: `$ (myvenv) pip3 install tg.devtools`
4. Open previously cloned repository and install project dependencies: `$ (myvenv) pip3 install -e .`
5. Setup project configurations, including DB creation: `$ (myvenv) gearbox setup-app`
> * See the note below
6. Start AxantAddressBook: `$ (myvenv) gearbox serve`
7. Open browser at `http://localhost:8080`
### Note about registration
In order to send mails upon registration completation, it's necessary to configure following params in `development.ini` with yours:
```
mail.host = ... 
mail.port = ... # intended TLS port
mail.username = ...
mail.password = ...
```

## `master` VS `core` branches
As the name suggests, *core* branch contains only core functionalities, without authentication setup. It can be seen as a "global address book", where anyone can see and add contacts.
If you create contacts in *master* with 2 different accounts and then `checkout` to *core*, you're able to see contacts of both.
Another important difference is that, at the time of writing, **unit testing is not working on _master_**. That because I didn't manage to mock authentication, despite
[docs](https://turbogears.readthedocs.io/en/latest/turbogears/testing.html#simulating-authentication-requests) are really clear about it.
I tried to mock the identity object of `repoze.who` with only fields I check against in template, but it does not work. I'll keep trying to find a solution. A pull request solving my doubts would be really appreciated.

### Unit testing
So, that's how you can run test:
1. **Use _core_ branch**: `$ git checkout core`
2. Install Python's utility for tests: `$ (myenv) pip3 install nose`
3. In the root of project run: `$ (myenv) python3 setup.py nosetests`
