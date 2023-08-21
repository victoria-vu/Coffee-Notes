# Coffee Notes ☕️
Coffee Notes is an dynamic full-stack application that allows users to search for coffee shops by coffee shop name or keyword and location parameters. Users can curate their own collection of favorite coffee shops through a bookmarking feature and craft personalized notes to each of their bookmarks. Whether users are on the hunt for a new brew or want to remember their past orders, Coffee Notes offers a seamless and organized way to savor every sip.

## Table of Contents
1. [Technologies Used](#technologies-used)
2. [How to Run Coffee Notes Locally](#how-to-run-coffee-notes-locally)
3. [Key Features](#key-features)
4. [Future Improvements](#future-improvements)

## Technologies Used
- Backend: Python, Flask, SQL, PostgresQL, SQLAlchemy
- Frontend: JavaScript, HTML/CSS, Bootstrap, JSON, Jinja2, AJAX
- APIs: Yelp Fusion API and Google Maps API
- UI Design: Figma
- Data Model: DBDesigner
  
<img width="800" alt="Screenshot 2023-08-20 at 7 47 15 PM" src="https://github.com/victoria-vu/Coffee-Project/assets/120001666/00f006ae-ff27-485a-8361-d2c92d482716">

## How to Run Coffee Notes Locally
1. To run Coffee Notes locally, clone this repository:
```
git clone https://github.com/victoria-vu/Coffee-Project.git
```
2. Create and activate a virtual environment within your terminal:
```
virtualenv env
source env/bin/activate
```
3. Install the requirements/dependencies:
```
pip3 install -r requirements.txt
```
4. Obtain a Yelp Fusion API Key from [Yelp Developer Portal](https://docs.developer.yelp.com/docs/fusion-authentication)
and a Google Maps API Key from [Google Maps Platform](https://developers.google.com/maps/documentation/javascript/get-api-key).

5. Create a secret.sh file and include the following line for the Yelp Fusion API Key:
```
export YELP_KEY="[your-key-goes-here]"
```
6. Add the secrets.sh file to .gitignore and load the API key to the shell environment:
```
$ source secrets.sh
```
7. Add the secured Google Maps API Key to cafe_details.html:
```
<script async src="[your-key-goes-here]"></script>
```
8. Set up the database:
```
python3 seed_database.py
```
9. Run the app:
```
python3 app.py
```
10. Navigate to [localhost:5000/](https:localhost:5000/) in your browser to use Coffee Notes! ☕️


## Key Features

### 💻 Create an account and log in.

<img width="800" alt="Screenshot 2023-08-21 at 11 43 48 AM" src="https://github.com/victoria-vu/Coffee-Project/assets/120001666/caacc3df-56f3-4b40-bfd9-b81b2689a00f">

Users can create an account using a unique email address, a password securely hashed to protect their data, and their full name. When logging in, the backend server will verify the user's credentials by cross-checking the entered email and password with the database. After successful authentication, the user's information will be stored in the session keys and the user will be redirected to their dashboard page. This ensures a personalized experience and allows coffee enthusiasts to access all the app's features to keep their coffee adventures organized.

### 🔍 Search for coffee shops by coffee shop name or keyword, and location.

<img width="800" alt="Screenshot 2023-08-21 at 11 54 02 AM" src="https://github.com/victoria-vu/Coffee-Project/assets/120001666/3e7f92e2-bdd6-481f-9cf2-dd3b86d812c2">

Users can search for coffee shops using either the coffee shop's name or keyword, and a location. On submission, the server will make a call to the Yelp Fusion API to fetch up-to-date and comprehensive information about nearby coffee shops. The results are then displayed on the page, allowing users to explore and discover various coffee shops.

### 🤎 View coffee shop details and save to your bookmarks page.

<img width="800" alt="Screenshot 2023-08-21 at 11 52 36 AM" src="https://github.com/victoria-vu/Coffee-Project/assets/120001666/7bad97a5-8b76-411a-90d6-9e9f452fdd3a">

Users can click on the "View More Details" button to view more information about a selected coffee shop and save the coffee shop to their bookmarks page.

### 📝 Make personalized notes on coffee shops for future reference.

<img width="800" alt="Screenshot 2023-08-21 at 11 56 09 AM" src="https://github.com/victoria-vu/Coffee-Project/assets/120001666/1a1f2f10-7cf8-4fca-baed-b7bdcc086668">

Users can access their bookmarks page to craft detailed and personalized notes on each bookmark. Whether it's jotting down favorite orders or sharing overall impressions, the user can turn their bookmarks page into their own personal digital diary. 

## Future Improvements
- Create a filtering feature to enhance search functionality.
- Integrate maps and location services to provide directions to the coffee shop from a user's current location.
- Allow users to create multiple bookmark lists for different purposes.
