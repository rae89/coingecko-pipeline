#!/usr/bin/env bash

/usr/local/bin/python /coin_gecko/coingecko/setup_db.py
/usr/local/bin/python /coin_gecko/coingecko/assets.py
/usr/local/bin/python /coin_gecko/coingecko/prices.py
