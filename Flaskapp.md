## Build a simple “Hello World” Flask app

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
```

<img width="887" height="329" alt="image" src="https://github.com/user-attachments/assets/58d9c913-abc7-42a7-8933-930e8856fc38" />

### What’s actually happening (brief, no fluff)

- `Flask(__name__)` → creates the app instance
- `@app.route('/')` → maps the URL `/` to a function
- `home()` → returns the response (a string → sent as HTML)
- `app.run()` → starts a local development server
