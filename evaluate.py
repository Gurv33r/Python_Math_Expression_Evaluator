ops='*','+'
import re

def chop(delimiters, string, maxsplit=0):
  """augmented version of split() function that takes mulitple delimiters as a tuple"""
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)
    
def paren_content(expr):
  """returns a list of the term in each set of parenthenses inside the input sorted by how nested in parentheses the term is"""
    stack = []
    tmap = {}
    for i,c in enumerate(expr):
        if c == '(':
            stack.append(i);
        elif c == ')' and stack:
            start = stack.pop()
            term = expr[start+1:i]
            if len(term)>0:
                term = term[1:len(term)-1] if term[0] == '(' and term[-1] == ')' else term
                if tmap.get(term):
                    tmap[term] += len(stack)
                else:
                    tmap[term] = len(stack)
    return sorted(tmap.items(), key =
            lambda kv:(len(kv[0]), kv[1]))

def label_negs(expr):
  """processes input and replaces the '-' in negative numbers with an 'n', which helps in precessing subtraction and negative numbers in general"""
    for i in range(len(expr)):
        if i == 0 and expr[i] == '-':
            expr = 'n' + expr[i+1:]
        elif expr[i] == '-':
            if expr[i-1] in '(+*':
                expr = expr[:i] + 'n' + expr[i+1:]
            elif i+1 < len(expr) and expr[i+1] in '-n':
                expr = expr[:i] + '+' + expr[i+2:]
            else:
                expr = expr[:i] + '+n' + expr[i+1:]
    return expr.replace('nn', '')

class ExpressionEvaluator:
    # Evaluates the expression and finds the result
    def evaluate(self, expr):
        expr = label_negs(expr.replace(' ', '')) # remove all whitespacea and label all negatives
        while '(' in expr or ')' in expr or '+' in expr or '-' in expr or '*' in expr: # exit condition = when expression is just a number
            expr = label_negs(expr) # ensure that all negative numbers are labeled
            term_list = paren_content('('+expr+')') # extract all terms from parentheses
            if len(term_list)>=1: # if there exists content within the parentheses
                prev_term = term_list[0][0] # prev_term will be used to determine if the level of the processed terms (determined by how nested in parentheses it is) has changed
                for t in term_list:
                    term = t[0] # access the term, not the level
                    if len(prev_term) < len(term): # if the level has changed, restart the loop
                        break
                    else:
                        #determine result
                        result = 0
                        operands = []
                        tokens = chop(ops, term) #find all operands in the term
                        if len(tokens) == 1:
                            # 1 operand case = remove its parentheses, if it has any
                            expr = expr.replace('(' + tokens[0] + ')', tokens[0])
                        elif len(tokens) == 2:
                          # 2 operands case = do the actual math
                          # subtraction is treated as adding a negative number, which gets covered in the label_negs funciton 
                            if '*' in term: # multiplication case
                                o = term.replace('n','-') # o = the mathmatically correct string version of the term
                                operands = list(map(int, o.split('*'))) # extract the operands as ints
                                result = str(operands[0] * operands[1]) # set the result to the string version of product of the operands
                            elif '+' in term: # addition case = same as multiplication case but finding the sum of the operands instead
                                o = term.replace('n','-')
                                operands = list(map(int, o.split('+')))
                                result = str(sum(operands))
                            expr = expr.replace(term, result) # replace the orginal term with the new result, any new negatives will be handled by label_negs
                        elif len(tokens) > 2:
                          # 3+ operands case = find a 2-operand term based on order of operations and put parentheses around it (let it get handled by the next iteration)
                            opi = 0 # will represent the index of the operation of the term to be parenthesized (i can't believe that's a real word)
                            if '*' in term: # multiplcation takes precedence over addtion
                                opi = expr.index(term) + term.index('*') # assign opi to the first '*' found
                            else: # no multiplication to evaluate? then pick the leftmost term since all that's left is addition and order of operations dictates left to right
                                opi = expr.index(term) + term.index(tokens[0]) + len(tokens[0])  # assign opi to the left most '+'
                            # now find the operands
                            j = opi-1 # will equal the left most index of operand 1
                            k = opi+1 # will equal the right most index of operand 2
                            while j-1>=0 and expr[j-1] not in ['(', '+', '-', '*']:
                                    j-=1
                            while k+1<len(expr) and expr[k+1] not in [')', '+', '-', '*']:
                                    k+=1
                            sub_term = expr[j:k+1] # sub_term is the term we are looking for
                            expr = expr.replace(sub_term, '(' + sub_term + ')') # replace sub_term in the expression with (sub_term)
                        prev_term = term # change prev_term
            else:
                if not expr.isnumeric():
                    expr = '(' + expr + ')' 
        #eventually the expression will break down into a single number that can contain a negative label, so before returing the answer, swap out the label for the negative sign
        return expr.replace('n','-')

def main():
    # Take Input
    expr = input()
    
    # Print result
    result = ExpressionEvaluator().evaluate(expr)
    print(f"{result}: {expr}")

# Call the main method
main()
