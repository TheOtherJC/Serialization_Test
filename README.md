# Synopsis


**Pickle**
   * Pickle serialises the object first before writing it to a file, which seems to very useful for what we're trying to do.
   
**Protobuf**
   * Protobuf doesn't deal with schema evolution which would cause most to assume it would be more efficient, yet is the least efficient out of the three choices.
    
**MsgPack**
   * Msgpack can distinguish string and binary type, yet it doesn't work well with Python 2 which could be a hindrance. However it does produce the shortest string length and is the quickest out the three.

# Installation
**Pickle:**

`import pickle`

**Protobuf:**

`$ sudo pip3 install protobuf`

`syntax = "proto2"`

**MsgPack:**

`$ sudo pip install msgpack-python`

`import msgpack`
# Motivation

