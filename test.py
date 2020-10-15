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
}

alpha = [];
beta = [];
beta = addNumbers(alpha, nextNumber(alpha));
gamma = beta;
'''
lexer = Lexer(text)
next_token = lexer.get_next_token()
while next_token.type != 'EOF':
    #print(next_token)
    next_token = lexer.get_next_token()
lexer.pos = 0
parser = Parser(lexer)
parsed = parser.parse()
#print(parsed)
'''nextNumber(num) {
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
'''
0: JumpOp(1, 1000, 1000)


1: something // num
2: ClearOp(3)
3: something
4: AddOp(1, 3) // make 3 = [num]
5: something
6: BinOp(+, 1, 4, 5) // make 5 = num + [num]


7: something // num1
8: something // ans
9: MovOp(7, 8) // make ans = num1
10: something // countNum2
11: ClearOp(10) // countNum2 = []
12: something
13: something // num2
14: BinOp(~, 10, 13, 12) // 12 = countNum2 ~ num2
15: JumpOp(12, 22, 16)
16: nextNumber(10) // ?????????
17: MovOp(16, 11) // countNum2 = nextNumber(counNum2)
18: nextNumber(8) // ??????????
19: MovOp(18, 8) // ans = nextNumber(ans)
20: BinOp(~, 10, 13, 12)
21: JumpOp(12, 22, 16)
'''
