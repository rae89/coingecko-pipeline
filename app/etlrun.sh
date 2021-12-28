#!/usr/bin/env bash

/usr/local/bin/python /coingecko/coingecko/setup_db.py
/usr/local/bin/python /coingecko/coingecko/assets.py
/usr/local/bin/python /coingecko/coingecko/prices.py
