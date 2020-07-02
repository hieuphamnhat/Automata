%{
#include "calc.tab.h"
#include <stdlib.h>
#include <stdio.h>
#define YY_DECL int yylex()
%}

white [[:blank:]\r]+
var [a-zA-Z_][a-zA-Z0-9]*
integer [0-9]+

%%

{white}
{var} {sscanf(yytext, "%s", yylval.name); return(VAR);}
{integer} { yylval.val=atof(yytext);return NUMBER;}

"=" return EQUAL;
"+" return PLUS;
"-" return MINUS;
"*" return TIMES;
"/" return DIVIDE;
%%
