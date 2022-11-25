grammar Sygus;

start       :   prog
            ;

prog        :   setWeightCmd cmdPlus 
            ;

setLogicCmd :   '(' 'set-logic' SYMBOL ')'
            ;

weightPlus   :   weightPlus '(' SYMBOL weight ')'
            |   '(' SYMBOL weight ')'
            ;

weight       :   'TROP'  |   'PROB'  |   'BOOL'
            ;

setWeightCmd    :   '(' 'set-weight' weightPlus ')'
                ;

cmdPlus     :   cmdPlus cmd
            |   cmd
            ;

cmd         :   setLogicCmd
            |   funDefCmd
            |   funDeclCmd
            |   synthFunCmd
            |   checkSynthCmd
            |   constraintCmd
            |   sortDefCmd
            |   setOptsCmd
            |   weightConstraintCmd
            |   weightOptimizationCmd
            |   varDeclCmd
            ;

weightOptimizationCmd   :   '(' 'optimize' weightPair ')'
                        ;

weightPair  :   '(' SYMBOL symbolPlus ')'
            |   SYMBOL
            ;


weightConstraintCmd     :   '(' 'weight-constraint' term ')'
                        ;

varDeclCmd  :   '(' 'declare-var' SYMBOL sortExpr ')'
            ;

sortDefCmd  :   '(' 'define-sort' SYMBOL sortExpr ')'
            ;

sortExpr    :   '(' 'BitVec' INTCONST ')'
            |   'Bool'
            |   'Int'
            |   'Real'
            |   '(' 'Enum' ecList ')'
            |   '(' 'Array' sortExpr sortExpr ')'
            |   SYMBOL
            ;

boolConst   :   'true' | 'false'
            ;

enumConst   :   SYMBOL '::' SYMBOL
            ;

ecList      :   '(' symbolPlus ')'
            ;

symbolPlus  :   symbolPlus SYMBOL
            |   SYMBOL
            ;

setOptsCmd  :   '(' 'set-options' optList ')'
            ;

optList     :   '(' symbolPairPlus ')'
            ;

symbolPairPlus  :   symbolPairPlus symbolPair
                |   symbolPair
                ;

symbolPair  :   '(' SYMBOL QUOTEDLIT ')'
            ;

funDefCmd   :   '(' 'define-fun' SYMBOL argList sortExpr term ')'
            ;

funDeclCmd  :   '(' 'declare-fun' SYMBOL '(' sortStar ')' sortExpr ')'
            ;

sortStar    :   sortStar sortExpr
            |   /* epsilon */
            ;

argList     :   '(' symbolSortPairStar ')'
            ;

symbolSortPairStar  :   symbolSortPairStar symbolSortPair
                    |   /* epsilon */
                    ;

symbolSortPair      :   '(' SYMBOL sortExpr ')'
                    ;

term        :   '(' SYMBOL termStar ')'     # application
            |   literal                     # liter
            |   SYMBOL                      # symbol
            |   letTerm                     # let
            ;

letTerm     :   '(' 'let' '(' letBindingTermPlus ')' term ')'
            ;

letBindingTermPlus  :   letBindingTermPlus letBindingTerm
                    |   letBindingTerm
                    ;

letBindingTerm      :   '(' SYMBOL term ')'
                    ;

termStar    :   termStar term
            |   /* epsilon */
            ;

literal     :   INTCONST
            |   boolConst
            |   BVCONST
            |   enumConst
            |   REALCONST
            ;

ntDefPlus   :   ntDefPlus ntDef
            |   ntDef
            ;

ntDef       :   '(' SYMBOL sortExpr '(' gTermPlus ')' ')'
            ;

gTermPlus   :   gTermPlus gTermWeighted
            |   gTermWeighted
            ;

checkSynthCmd   :   '(' 'check-synth' ')'
                ;

constraintCmd   :   '(' 'constraint' term ')'
                ;

synthFunCmd :   '(' 'synth-fun' SYMBOL argList sortExpr '(' ntDefPlus ')' ')'
            ;

gTermWeighted   :   '(' gTerm ':' literalPlus ')'
                |   gTerm
                ;

literalPlus :   literalPlus literal
            |   literal
            ;


gTerm       :   SYMBOL
            |   literal
            |   '(' SYMBOL gTermStar ')'
            |   '(' 'Constant' sortExpr ')'
            |   '(' 'Vairiable' sortExpr ')'
            |   '(' 'InputVariable' sortExpr ')'
            |   '(' 'LocalVariable' sortExpr ')'
            |   letGTerm
            ;

letGTerm    :   '(' 'let' '(' letBindingGTermPlus ')' gTerm ')'
            ;

letBindingGTermPlus :   letBindingGTermPlus letBindingGTerm
                    |   letBindingGTerm
                    ;

letBindingGTerm :   '(' SYMBOL sortExpr gTerm ')'
                ;

gTermStar   :   gTermStar gTerm
            |   /* epsilon */
            ;

WS          :   [ \t\r\n\u000C]+ -> skip
            ;
fragment
LETTER      :   [a-zA-Z_]
            ;
fragment
DIGIT       :   [0-9]
            ;
fragment
HEXDIGIT    :   DIGIT
            |   [a-f]
            |   [A-F]
            ;
fragment
BIT         :   '0'
            |   '1'
            ;
fragment
INTEGER     :   '-'? DIGIT+
            ;

INTCONST    :   INTEGER
            ;

BVCONST     :   '#x'HEXDIGIT+
            |   '#b'BIT+
            ;

REALCONST   :   '-'? DIGIT+ '.' DIGIT+
            ;

fragment
SYMBOLCC    :   [a-z]
            |   [A-Z]
            |   '_'
            |   '+'
            |   '-'
            |   '*'
            |   '&'
            |   '|'
            |   '!'
            |   '~'
            |   '<'
            |   '>'
            |   '='
            |   '/'
            |   '%'
            |   '?'
            |   '.'
            |   '$'
            |   '^'
            ;

SYMBOL      :   SYMBOLCC (SYMBOLCC | DIGIT)*
            ;

QUOTEDLIT   :   '\'' ([a-z] | [A-Z] | DIGIT | '.') + '\''
            ;
