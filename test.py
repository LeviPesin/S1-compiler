from s1_lexer import *
from s1_parser import *
text = '''nextNumber(num) {
    return num + [num];
}

addNumbers(num1, num2) {
    ans = num1;
    countNum2 = [];
    whilene (countNum2 ~ num2) {
        countNum2 = nextNumber(countNum2);
        ans = nextNumber(ans);
    }
    return ans;
}

multiplyNumbers(num1, num2) {
    ans = [];
    countNum2 = [];
    whilene (countNum2 ~ num2) {
        countNum2 = nextNumber(countNum2);
        ans = addNumbers(ans, num1);
    }
    return ans;
}'''
lexer = Lexer(text)
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
##print(lexer.get_next_token())
parser = Parser(lexer)
parsed = parser.parse()
print(parsed)
print(parsed.blocks[0])
print(parsed.blocks[1])
print(parsed.blocks[2])
print(parsed.blocks[0].name)
print(parsed.blocks[0].pars)
print(parsed.blocks[0].code)
print(parsed.blocks[0].code[0].expr)
print(parsed.blocks[0].code[0].expr.left)
print(parsed.blocks[0].code[0].expr.op)
print(parsed.blocks[0].code[0].expr.right)
print(parsed.blocks[0].code[0].expr.right.pars[0])
print(parsed.blocks[0].code[0].expr.right.pars[0].name)
