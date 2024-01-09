#!/usr/bin/env python3
"""This script allows for the generation of an invite code.
"""
import argparse

from app.database.database import SessionLocal
from app.utils import generate_invite_code

argParser = argparse.ArgumentParser(prog="Generate invite code", description="Allows for the generation of an invite code to register")
argParser.add_argument("-e", "--expires_in", help="the time in minutes the code will expire", required=True, type=float)

args = argParser.parse_args()

expires_in = args.expires_in

db = SessionLocal()

code, expire_ts = generate_invite_code(db=db, expires_in=expires_in)

print(f"INVITE CODE: {code}")
print(f"EXPIRES: {expire_ts}")
