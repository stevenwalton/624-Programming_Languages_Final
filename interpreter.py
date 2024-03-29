import ply.lex as lex
import ply.yacc as yacc
from ctokens import *

# Print out tree and contents of p at each step
DEBUG=True
#DEBUG=False

lexer = lex.lex()

def is_number(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def p_interpreter_block(p):
    '''
    interpreter_block : EOF
                      | interpreter_multiple_block EOF
    '''
    if DEBUG:
        print("\ninterp_block: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = p[1]
    # Do we need to do EOF?

def p_interpreter_multiple_block(p):
    '''
    interpreter_multiple_block : statement
                               | function_decl
                               | statement interpreter_multiple_block
                               | function_decl interpreter_multiple_block
    '''
    if DEBUG:
        print("\ninterp_mult_block: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = (p[1],p[2])
    else:
        p[0] = p[1]


def p_compound_statement(p):
    '''
    compound_statement : LBRACE RBRACE
                       | LBRACE multiple_statement RBRACE
    '''
    if DEBUG:
        print("\ncompound stmt: ",end="")
        # Note: Nests the statements
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = p[2]
    #if p[1] == '{':
    #    if p[2] != '}':
    #        p[0] = p[2]
    #elif len(p) > 2:
    #    p[0] = (p[1],p[2])
    #else:
    #    p[0] = p[1]

def p_multiple_statement(p):
    '''
    multiple_statement : statement
                       | statement multiple_statement
    '''
    if DEBUG:
        print("\nmultiple statement: ",end="")
        # Note: Nests the statements
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = (p[1],p[2])
    else:
        p[0] = p[1]

def p_statement(p):
    '''
    statement : compound_statement
              | expr_statement
              | selection_statement
              | for_statement
              | do_while_statement
              | while_statement
              | jump_statement
              '''
    #          | open_statement
    #          | closed_statement
    #'''
    if DEBUG:
        print("\nstatement: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[1]

######
# Commented for debugging
######
def p_open_statement(p):
    '''
    open_statement : IF LPAREN expr RPAREN statement
                   | IF LPAREN expr RPAREN closed_statement ELSE open_statement
    '''
    if DEBUG:
        print("\nopen stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    # This one needs to be checked
    # if len(p) > 5:
    #     if p[3]:
    #         p[0] = p[5]
    #     else:
    #         p[0] = p[7]
    # else:
    #     if p[3]:
    #         p[0] = p[5]
    if len(p) == 6:
        p[0] = (p[1], p[3], p[5])
    elif len(p) == 8:
        p[0] = ("IF_ELSE", p[3], p[5], p[7])
#   
# FIX
def p_closed_statement(p):
    '''
    closed_statement : statement
                     | IF LPAREN expr RPAREN closed_statement ELSE closed_statement
    '''
    if DEBUG:
        print("\nclosed stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ("If_ELSE", p[3],p[5],p[7])
    #if p[3]:
    #    p[0] = p[5]
    #else:
    #    if len(p) > 5:
    #        p[0] = p[7]

def p_expr_statement(p):
    '''
    expr_statement : SEMI
                   | assignment_expr SEMI
    '''
    if DEBUG:
        print("\nexpr stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if p[1] != ';':
        p[0] = p[1]


#####
# Requires a ";" after the ")" of the "if" expression and after the "else" to work
#####
def p_selection_statement(p):
    '''
    selection_statement : IF LPAREN expr RPAREN compound_statement
                        | IF LPAREN expr RPAREN closed_statement ELSE statement
    '''
    #'''
    #selection_statement : IF LPAREN expr RPAREN statement
    #                    | IF LPAREN expr RPAREN statement ELSE statement
    #'''
    if DEBUG:
        print("\nselection statement: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 6:
        p[0] = (p[1],p[3],p[5])
    else:
        p[0] = ("IF_ELSE",p[3],p[5],p[7])
    #if p[3]:
    #    p[0] = p[5]
    #else:
    #    if len(p) > 5:
    #        p[0] = p[7]


def p_for_statement(p):
    '''
    for_statement : FOR LPAREN ID IN expr RPAREN statement
    '''
    if DEBUG:
        print("\nfor stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = (p[1],p[3],p[5],p[7])


def p_do_while_statement(p):
    '''
    do_while_statement : DO statement WHILE LPAREN expr RPAREN SEMI
    '''
    if DEBUG:
        print("\ndo while stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ("DO_WHILE", p[2],p[5])

def p_while_statement(p):
    '''
    while_statement : WHILE LPAREN expr RPAREN statement
    '''
    if DEBUG:
        print("\nwhile stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = (p[1],p[3],p[5])

def p_jump_statement(p):
    '''
    jump_statement : NEXT SEMI
                   | BREAK SEMI
                   | RETURN SEMI
                   | RETURN expr SEMI
    '''
    if DEBUG:
        print("\njmp stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = (p[1],p[2])
    else:
        p[0] = p[1]

def p_expr(p):
    '''
    expr : conditional_expr
    '''
    if DEBUG:
        print("\nexpr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[1]

def p_assignment_expr(p):
    '''
    assignment_expr : conditional_expr
                    | conditional_expr EQUALS conditional_expr
    '''
    if DEBUG:
        print("\nassignment expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    # only w/ constant
    if len(p) == 4:
        p[0] = (p[2],p[1],p[3])
    else:
        p[0] = p[1]

def p_conditional_expr(p):
    '''
    conditional_expr : logical_or_expr
                     | conditional_else_expr
    '''
    if DEBUG:
        print("\ncond expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[1]

def p_conditional_else_expr(p):
    '''
    conditional_else_expr : logical_or_expr TERNARY conditional_expr ELSE conditional_expr
    '''
    if DEBUG:
        print("\nConditional Else: ",end="")
        # Note: doesn't have "ELSE"
        p[0] = ("?", p[1], p[3],p[5])
        #p[0] = ("IF_ELSE", p[1], p[3],p[5])

def p_logical_or_expr(p):
    '''
    logical_or_expr : logical_and_expr
                    | logical_and_expr OR or_multiple
    '''
    if DEBUG:
        print("\nor expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    # only w/ constant
    l = len(p)
    if l == 4:
        p[0] = (p[2],p[1], p[3])
    else:
        p[0] = p[1]
    #if l == 2:
    #    p[0] = p[1]
    #elif l == 3:
    #    p[0] = (p[1],p[2])
    #elif l == 4:
    #    p[0] = (p[2],p[1],p[3])

def p_or_multiple(p):
    '''
    or_multiple : logical_and_expr
                | logical_and_expr OR or_multiple
    '''
        #or_multiple : or_multiple OR logical_and_expr
    if DEBUG:
        print("\nor mult expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    l = len(p)
    if l == 4:
        p[0] = (p[2],p[1],p[3])
    else:
        p[0] = p[1]
    #if l == 4:
    #    p[0] = (p[2],p[1],p[3])
    #else:
    #    p[0] = (p[1],p[2])

def p_logical_and_expr(p):
    '''
    logical_and_expr : equality_expr
                     | equality_expr AND and_multiple
    '''
    #   and_multiple : and_multiple AND equality_expr
    #                | AND equality_expr
    #'''
    if DEBUG:
        print("\nand expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    l = len(p)
    if l == 4:
        p[0] = (p[2],p[1],p[3])
    else:
        p[0] = p[1]
    #if l == 2:
    #    p[0] = p[1]
    #elif l == 3:
    #    p[0] = (p[1],p[2])
    #elif l == 4:
    #    p[0] = (p[2],p[1],p[3])
    ## Hacky way. Should break things up
    #try:
    #    if p[1] == '&':
    #        p[0] = p[2]
    #    else:
    #        # Check p[1]
    #        if p[1] == 'T':
    #            p[1] = True
    #        elif p[1] == 'F':
    #            p[1] = False
    #        else:
    #            pass

    #        # Check p[2]
    #        if p[2] == 'T':
    #            p[2] = True
    #        elif p[2] == 'F':
    #            p[2] = False
    #        else:
    #            pass

    #        if p[1] and p[2]:
    #            p[0] = t_TRUE
    #        else:
    #            p[0] = t_FALSE
    #except:
    #    p[0] = p[1]
def p_and_multiple(p):
    '''
       and_multiple : equality_expr
                    | equality_expr AND and_multiple
    '''
    if DEBUG:
        print("\nand mult expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    l = len(p)
    if l == 4:
        p[0] = (p[2],p[1],p[3])
    else:
        p[0] = p[1]


def p_equality_expr(p):
    '''
    equality_expr : relational_expr
                  | relational_expr NE equality_multiple
                  | relational_expr EQ equality_multiple
    '''
    if DEBUG:
        print("\nequality expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = (p[2],p[1],p[3])
    else:
        p[0] = p[1]

def p_equality_multiple(p):
    '''
    equality_multiple : relational_expr
                      | relational_expr NE equality_multiple
                      | relational_expr EQ equality_multiple
    '''
    if DEBUG:
        print("\nequality multiple expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = (p[2],p[1],p[3])
    else:
        p[0] = p[1]


def p_relational_expr(p):
    '''
    relational_expr : add_expr
                    | add_expr LT relational_multiple
                    | add_expr LE relational_multiple
                    | add_expr GT relational_multiple
                    | add_expr GE relational_multiple
    '''
    if DEBUG:
        print("\nrelational expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = (p[1],p[2])
    else:
        p[0] = p[1]

def p_relational_multiple(p):
    '''
    relational_multiple : add_expr
                        | add_expr LT relational_multiple
                        | add_expr LE relational_multiple
                        | add_expr GT relational_multiple
                        | add_expr GE relational_multiple
    '''
    if DEBUG:
        print("\nrelational multiple expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = (p[2],p[1],p[3])
    else:
        p[0] = p[1]
    #if len(p) == 4:
    #    p[0] = (p[2],p[1],p[3])
    #else:
    #    p[0] = (p[1],p[2])


def p_add_expr(p):
    '''
    add_expr : mult_expr
             | add_expr PLUS mult_expr
             | add_expr MINUS mult_expr
    '''
    if DEBUG:
        print("\nadd expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = (p[2],p[1],p[3])
        if p[2] == '+':
            try:
                p[1] = float(p[1])
                p[3] = float(p[3])
            except ValueError:
                print("Not a number\n")
            else:
                p[0] = p[1] + p[3]
        elif p[2] == '-':
            try:
                p[1] = float(p[1])
                p[3] = float(p[3])
            except:
                print("Not a number\n")
            else:
                p[0] = p[1] - p[3]
        else:
            print("Not a valid add expression operator!\n")
    else:
        p[0] = p[1]
    #if len(p) < 3:
    #  p[0] = p[1]
    #else:
    #  p[0] = (p[2], p[1], p[3])

def p_mult_expr(p):
    '''
    mult_expr : seq_expr
              | seq_expr TIMES mult_expr
              | seq_expr DIVIDE mult_expr
              | seq_expr MODULO mult_expr
    '''
    if DEBUG:
        print("\nmult expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
        if p[2] == '*':
            try:
                p[1] = float(p[1])
                p[3] = float(p[3])
            except ValueError:
                print("Not a number\n")
            else:
                p[0] = p[1] * p[3]
        elif p[2] == '/':
            try:
                p[1] = float(p[1])
                p[3] = float(p[3])
            except:
                print("Not a number\n")
            else:
                p[0] = p[1] / p[3]
        elif p[2] == '%':
            try:
                p[1] = float(p[1])
                p[3] = float(p[3])
            except:
                print("Not a number\n")
            else:
                p[0] = p[1] % p[3]
        else:
            print("Not a valid mult expression operator!\n")
    else:
        p[0] = p[1]
    # if len(p) <= 3 :
    #     p[0] = p[1]
    # elif p[2] == '*':
    #     p[0] = p[1] * p[3]
    # elif p[2] == '/':
    #     p[0] = p[1] / p[3]
    # elif p[2] == '%':
    #     p[0] = p[1] % p[3]
    # else:
    #     print("ERROR!!! Don't know symbol: ",p[2])

def p_seq_expr(p):
    '''
    seq_expr : exp_expr
             | exp_expr COLON exp_expr
    '''
    if DEBUG:
        print("\nseq expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = (p[2],p[1],p[3])
    else:
        p[0] = p[1]

def p_exp_expr(p):
    '''
    exp_expr : unary_expr
             | unary_expr XOR exp_expr
    '''
    if DEBUG:
        print("\nexp expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = (p[2],p[1],p[3])
    else:
        p[0] = p[1]

def p_unary_expr(p):
    '''
    unary_expr : postfix_expr
               | NOT unary_expr
               | PLUS unary_expr
               | MINUS unary_expr
    '''
    if DEBUG:
        print("\nunary expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = (p[1],p[2])
    else:
        p[0] = p[1]

# Split this into 3!!!
def p_postfix_expr(p):
    '''
    postfix_expr : primary_expr
                 | primary_expr expr_array
                 | primary_expr argument_array
                 | primary_expr object_call
    '''
    if DEBUG:
        print("\npostfix expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = (p[1],p[2])
    else:
        p[0] = p[1]

# We left out leading comma case (,exp,exp) and (,) because they are dumb
#   and should result in errors
def p_expr_array(p):
    '''
    expr_array : LBRACKET RBRACKET
               | LBRACKET expr RBRACKET
               | LBRACKET expr COMMA RBRACKET
               | LBRACKET expr COMMA expr RBRACKET
               | LBRACKET multi_expr RBRACKET
               | LBRACKET COMMA multi_expr RBRACKET
    '''
    if DEBUG:
        print("\nexpr_array: ",end="")
    if len(p) == 6: # LBRACKET expr COMMA expr RBRACKET
        p[0] = (p[3],p[2],p[4])
    elif len(p) == 5 and p[2] == ',': # LBRACKET COMMA multi_expr RBRACKET
        p[0] = (p[2],p[3])
    elif len(p) == 5 and p[3] == ',': # LBRACKET expr COMMA RBRACKET
        p[0] = (p[3],p[2])
    elif len(p) == 4: # LBRACKET expr RBRACKET
        p[0] = p[3]
    else:
        pass
        
def p_multi_expr(p):
    '''
    multi_expr : expr COMMA multi_expr
               | expr COMMA
               | expr
    '''
    if DEBUG:
        print("\nmulti_expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    l = len(p)
    if l == 4:
        p[0] = (p[2],p[1],p[3])
    elif l == 3:
        p[0] = (p[2],p[1])
    else:
        p[0] = p[1]

def p_argument_array(p):
    '''
    argument_array : LPAREN RPAREN
                   | LPAREN argument_expr_list RPAREN
    '''
    if DEBUG:
        print("\nargument array: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = p[2]
    else:
        pass

def p_object_call(p):
    '''
    object_call : PERIOD ID
    '''
    if DEBUG:
        print("\nobject call: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = (p[1],p[2])

def p_primary_expr(p):
    '''
    primary_expr : constant
                 | ID
                 | LPAREN expr RPAREN
    '''
    if DEBUG:
        print("\nprimary expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_argument_expr_list(p):
    '''
    argument_expr_list : argument_expr
                       | argument_expr COMMA argument_expr_list
    '''
    if DEBUG:
        print("\nargument expr lst: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = (p[2],p[1],p[3])
    else:
        p[0] = p[1]

def p_argument_expr(p):
    '''
    argument_expr : conditional_expr
                  | ID EQUALS conditional_expr
    '''
    if DEBUG:
        print("\nargument expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = (p[2],p[1],p[3])
    else:
        p[0] = p[1]

def p_constant(p):
    '''
    constant : INTEGER
             | FLOAT
             | STRING
             | CHARACTER
             | TRUE
             | FALSE
    '''
    if DEBUG:
        print("\nconst: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[1]



def p_function_decl(p):
    '''
    function_decl : FUNCTION return_type_spec ID param_list compound_statement
    '''
    if DEBUG:
        print("\nfun decl: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    # Don't think this is right
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_return_type_spec(p):
    '''
    return_type_spec : LPAREN type_spec RPAREN
    '''
    if DEBUG:
        print("\nreturn type spec: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[2]

# Split into two
def p_type_spec(p):
    '''
    type_spec : type_spec_options
              | type_spec_options DOLLAR
    '''
    if DEBUG:
        print("\ntype spec: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[1] # Do I need $? No


#Do we want to include the singleton types?
def p_type_spec_option(p):
    '''
    type_spec_options : TYPEVOID
                      | TYPENULL
                      | TYPELOGICAL
                      | TYPEINTEGER
                      | TYPEFLOAT
                      | TYPESTRING
                      | TYPEOBJECT
                      | TYPEOBJECT object_class_spec
                      | TYPENUMERIC
                      | PLUS
                      | TIMES
    '''
    if DEBUG:
        print("\ntype spec option: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = (p[1],p[2]) #???
    else:
        p[0] = p[1]

def p_object_class_spec(p):
    '''
    object_class_spec : GT ID LT
    '''
    if DEBUG:
        print("\nobject class spec: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[2]


# Split into 3
def p_param_list(p):
    '''
    param_list : LPAREN param_option RPAREN
    '''
    #param_option : TYPEVOID
    #             | param_spec
    #             | param_spec param_spec_multiple
    #param_spec_multiple : COMMA param_spec
    #                    | param_spec_multiple COMMA param_spec
    #'''
    if DEBUG:
        print("\nparam list: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[2]
    #for i in range(len(p)):
    #    print(i," ",p[i], " ",end="")
    #if p[1] == '(' and p[3] == ')':
    #    p[0] = p[2]
    #elif p[1] == ',':
    #    p[0] = p[2]
    #elif p[2] == ',':
    #    p[0] = (p[1],p[3])
    #else:
    #    p[0] = p[1]

def p_param_option(p):
    '''
    param_option : TYPEVOID
                 | param_spec
                 | param_spec param_spec_multiple
    '''
    if DEBUG:
        print("\nparam option: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = (p[1],p[2])
    else:
        p[0] = p[1]

def p_param_spec_multiple(p):
    '''
    param_spec_multiple : COMMA param_spec
                        | param_spec_multiple COMMA param_spec
    '''
    if DEBUG:
        print("\nparam spec mult: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = (p[1],p[3]) 
    else:
        p[0] = p[2]


#####################
## Checked up to here
#####################
# FIX
# Needs type checking eventually
def p_param_spec(p):
    '''
    param_spec : type_spec ID
               | LBRACKET type_spec ID EQUALS value_option RBRACKET
    '''
    if DEBUG:
        print("\nparam spec: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 7:
        p[0] = (p[4],p[2],p[3],p[5])
    else:
        p[0] = (p[1],p[2])

def p_value_option(p):
    '''
    value_option : constant
                 | ID
    '''
    if DEBUG:
        print("\nvalue option: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[1]

def p_eof(p):
    '''
    EOF :
    '''
    pass
    #return p[0]

# prog = input("input here:\n",end="")

#prog = 'c(1,2,3);'
#prog = 'if (if(F)); break;'
# This works, but not else if
#prog = 'if (if(F));something; else; break;'
#prog = 'if (F) x=12;'
#prog = 'if (F); break;'
#prog = 'if (F); break; else; x=42;'
#prog = 'cmColors(0);'
#prog = 'integerDiv(6, y=3);'
#prog = 'T==F;'
#prog = 'T | F;'
#prog = 'T & F;'

prog = 'x=x+2;'


parser = yacc.yacc()
result = parser.parse(prog, debug=False)
if DEBUG:
    print("\n=====\nDONE\n=====")
    print("Parsed: ", end="")
    print(prog)
    print("Result: ",result)
else:
    print(result)
