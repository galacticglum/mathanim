#pragma once

#define FIRST_ARG_ (N, ...) N
#define FIRST_ARG (args) FIRST_ARG_ args
#define XSTR(S) STR(S)
#define STR(S) #S