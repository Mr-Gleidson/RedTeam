# XSS Vulnerability Testing Tool

This is a Python code that allows you to test Cross-Site Scripting (XSS) vulnerabilities in a web application. XSS is a common security vulnerability that enables an attacker to inject malicious code into a web application, which is then executed in a user's browser.

## How to Use

1. Ensure you have Python installed on your system.
2. Download the code and save it to a Python file, for example, `scanner-xss.py`.

## Run the code as follows:
```
python scanner-xss.py [URL] [PAYLOADS_FILE] [VULNERABILITY_TYPE] [INJECTION_POINT] [HTTP_METHOD] [ENCODING]
```

`[URL]`: The URL of the web application you want to test.
<br>
`[PAYLOADS_FILE]`: The path to a text file containing XSS payloads you want to test.
<br>
`[VULNERABILITY_TYPE]`: The type of vulnerability you want to test (reflected or persistent).
<br>
`[INJECTION_POINT]`: The injection point you want to test (url, header, Cookie, javascript).
<br>
`[HTTP_METHOD]`: The HTTP method you want to use (get or post).
<br>
`[ENCODING]`: The encoding to apply to payloads (base64, url, or html).

## How It Works
The code makes HTTP requests to the specified URL with XSS payloads injected at specific injection points, such as URL, HTTP header, cookie, or JavaScript code. It uses payloads provided in a text file and allows you to test both reflected and persistent XSS vulnerabilities.

If an XSS vulnerability is found, the code will print a message indicating the vulnerable URL and the payload that succeeded. Otherwise, it will report that no XSS vulnerability was found.

## Notes
This code is a security testing tool and should be used only on systems for which you have testing permission.
Checking for XSS vulnerabilities is a complex task and may not detect all vulnerabilities. Additionally, testing vulnerabilities on systems without authorization may be illegal.
Always use this tool ethically and in compliance with local laws and regulations.
