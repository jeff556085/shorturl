ShortURL is a simple URL shortening service built with Python. 
It provides the ability to shorten long URLs into concise links that are easier to share.
The service can also enforce expiration (30 days by default), rate-limiting, and includes basic RESTful endpoints for integration with other services.

Short URL Generation
Converts any long URL into a shorter, more readable format.

Expiration Policy
Default link expiration after 30 days to avoid perpetually active short links.

Redirection
When a user visits the short link, it automatically redirects (HTTP 302) to the original URL.

RESTful API
Easy integration with front-end or third-party services.

Rate Limiting
Prevents abuse by limiting the number of requests from a single IP within a given time window.

Docker Container
Provides a Dockerfile for easy containerization and deployment.


Installation & Usage
1. Clone the Repository
git clone https://github.com/<your-username>/shorturl.git
cd shorturl

2. Install Dependencies
pip install -r requirements.txt

3. Start the Service
Depending on your setup, you might do something like:
python app/main.py

Then visit http://localhost:5000 (or the appropriate port) in your browser or API client to test.


