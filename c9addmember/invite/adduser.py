#!/usr/bin/env python
# coding: utf-8

# Imports
import urllib.request, os, sys
from http.cookiejar import CookieJar

USER_AGENT = "/kinoshitajona/c9community/add_users/script/v0.0.4"

def add_user(ADD_USER_EMAIL):
    try:
        USER_NAME = os.environ['C9_USER_NAME']
        PASSPHRASE = os.environ['C9_PASSPHRASE']
        TEAM_NAME = os.environ['C9_TEAM_NAME']
        
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)
        
        login_data = r'{"username": "' + USER_NAME + '", "password": "' + PASSPHRASE + '"}'
        
        req = urllib.request.Request("https://c9.io/auth/login",
                              data=login_data)
        
        req.add_header("User-Agent",USER_AGENT)
        req.add_header("Content-Type","application/json")
        req.add_header("Referer","https://c9.io/login")
        
        # Send the request here. We don't need anything from the response, just the cookies which are handled for us.
        result1 = urllib.request.urlopen(req)
        
        # Second request, this time we need a token this one is GET request as data=None
        req = urllib.request.Request("https://c9.io/api/nc/auth?client_id=profile_direct&responseType=direct&login_hint=&immediate=1")
        
        # Set headers again. Different referrer
        req.add_header("User-Agent",USER_AGENT)
        req.add_header("Content-Type","application/json")
        
        # Send GET request
        result2 = urllib.request.urlopen(req)
        
        # Read the token from the response.
        token = result2.read() # Token
        
        
        # text JSON data with the users email which you want to invite
        email_data = r'{"email": "' + ADD_USER_EMAIL + '"}'
        
        # this is a POST request to invite the email address to your team.
        req = urllib.request.Request("https://api.c9.io/user/org/" + TEAM_NAME + "/invite?access_token=" + token,
                              data=email_data)
        
        req.add_header("User-Agent",USER_AGENT)
        req.add_header("Content-Type","application/json")
        
        # Send the POST request
        result3 = urllib.request.urlopen(req)
    except:
        return False
    
    return True
