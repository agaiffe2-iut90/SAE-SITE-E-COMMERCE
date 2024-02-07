import os

from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from dotenv import load_dotenv

load_dotenv()

import pymysql.cursors



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        #
        db = g._database = pymysql.connect(
            host=os.environ.get("HOST"),
            # host="serveurmysql",
            user=os.environ.get("UTILISATEUR"),
            password=os.environ.get("PASSWORD"),
            database=os.environ.get("DATABASE"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return db