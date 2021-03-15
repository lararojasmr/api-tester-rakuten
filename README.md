## How to run this:

### You must pass two arguments:

**baseurl:** The url where the api is located.

**apiversion:** Identify the schema versions that the framework must use. For this example is: v1

**teamcity**: If you want to integrate with teamcity, just need to add this flag.

### _Local in terminal:_

pytest --baseurl https://protected-atoll-83840.herokuapp.com --apiversion
v1

### In Teamcity:

pytest --baseurl https://protected-atoll-83840.herokuapp.com --apiversion
v1 --teamcity