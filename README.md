# Flask OTP-Based Authentication App

This is a Flask web application that includes:
- User registration with email and password  
- Email-based OTP verification during signup  
- Login and logout functionality  
- Google reCAPTCHA (v2 checkbox) for bot protection  
- Secure session handling with expiration control  
- CSRF protection using Flask-WTF  
- Cache control to prevent back/forward access after logout  
- Styled frontend using custom CSS  

---

## Features

- OTP verification using Flask-Mail  
- Google reCAPTCHA integration for login and registration  
- CSRF protection using Flask-WTF  
- Password hashing with Flask-Bcrypt  
- Session timeout and browser-session control  
- Flash messaging for errors and feedback  
- Cache prevention to block unauthorized dashboard access  
- Styled HTML pages for Register, Login, OTP, and Dashboard  

---

## How to Run

1. Clone the repository  
2. Create and activate a virtual environment  
3. Install dependencies:

   ```bash
   pip install -r requirements.txt

   Create a `.env` file in the project root and add:

```
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password
RECAPTCHA_PUBLIC_KEY=your_site_key
RECAPTCHA_PRIVATE_KEY=your_secret_key
```

Ensure your reCAPTCHA configuration includes the following domains:

```
localhost
127.0.0.1
```

Run the application:

```
python app.py
```

Open in your browser:

```
http://127.0.0.1:5000/
```

Note:

- Use a Gmail App Password instead of your actual email password
- Do not upload the `.env` file to GitHub
- Add `.env` and `venv/` to your `.gitignore`


Screenshots
<img width="1919" height="1027" alt="Screenshot 2026-04-27 213812" src="https://github.com/user-attachments/assets/3e87fad0-1814-4279-95b7-1363764dd42c" />



<img width="1919" height="1031" alt="Screenshot 2026-04-27 213849" src="https://github.com/user-attachments/assets/e1c7d3dd-4008-485d-85a6-08fc7cb7c2f1" />



<img width="1901" height="901" alt="Screenshot 2025-09-25 191636" src="https://github.com/user-attachments/assets/32269212-9c51-4e1d-a2d9-2cc0dbd68e22" />



---
