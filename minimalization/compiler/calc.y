%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex();
int yyerror(char *s);
int checkName(char *s);
char var_name[20];

int value;
%}

%union {
    char name[20];
    int val;
}

%token NUMBER
%token VAR
%token EQUAL PLUS MINUS TIMES DIVIDE

%type<val> NUMBER  Expression
%type<name> VAR

%start Input
%%

Input:
	| Input Line
;

Line:
	Expression Expression { printf("%d\n",value); exit(0); }
;

Expression:
      VAR EQUAL NUMBER {sscanf($1, "%s", var_name); value = $3;}
	|VAR PLUS NUMBER { checkName($1); value = value + $3; }
	| VAR MINUS NUMBER { checkName($1); value = value - $3; }
	| VAR TIMES NUMBER { checkName($1); value = value * $3; }
	| VAR DIVIDE NUMBER { checkName($1); if($3 == 0){printf("Cannot DIVIDE for zero"); exit(1);}; value = value/$3; }
;

%%

int checkName(char *s1){
	if (strcmp(s1, var_name)) {
		printf("Variable \"%s\" is not error", s1);
		exit(1);
     };
}

int yyerror (char  *s) {
	printf("%s\n", s);
}

int main() {
  if (yyparse())
     fprintf(stderr, "Successful parsing.\n");
  else
     fprintf(stderr, "error found.\n");
}