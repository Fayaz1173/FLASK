# FLASK
## Flask Basics: Routing, Templates, and Request Handling

---

### 1. Routing

**Definition:**

Routing is the process of mapping a URL to a specific function in a Flask application.

**Key Points:**

- It determines what happens when a user visits a particular URL.
- Defined using `@app.route()` decorator.

**Example:**

```
fromflaskimportFlask
app=Flask(__name__)

@app.route('/')
defhome():
return"Hello, World!"

@app.route('/about')
defabout():
return"About page"
```

**Summary:**

Routing controls **which function runs for a given URL**.

---

### 2. Templates

**Definition:**

Templates are HTML files used to display dynamic content. Flask uses the Jinja2 template engine.

**Key Points:**

- Allows embedding Python variables inside HTML.
- Stored inside a `templates` folder.

**Example:**

**Python:**

```
fromflaskimportrender_template

@app.route('/')
defhome():
returnrender_template('index.html',name="Alice")
```

**HTML (index.html):**

```
<h1>Hello {{ name }}</h1>
```

**Summary:**

Templates are responsible for the **user interface (UI)**.

---

### 3. Request Handling

**Definition:**

Request handling refers to managing and processing data sent by the client (user).

**Key Points:**

- Flask provides a `request` object.
- Supports methods like GET and POST.

**Example (GET):**

```
fromflaskimportrequest

@app.route('/greet')
defgreet():
name=request.args.get('name')
returnf"Hello{name}"
```

**Example URL:**

```
/greet?name=John
```

---

**Example (POST):**

```
fromflaskimportrequest

@app.route('/submit',methods=['POST'])
defsubmit():
username=request.form['username']
returnf"Welcome{username}"
```

**Summary:**

Request handling is used to **receive and process user input**.

---

### Overall Flow in Flask

1. User visits a URL → **Routing**
2. Flask processes input → **Request Handling**
3. Flask returns a response → **Template Rendering**
