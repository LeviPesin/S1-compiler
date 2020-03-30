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
