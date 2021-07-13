import gurobipy as gp
from gurobipy import GRB
import numpy as np


class Class_solveQP:
    def __init__(self):
        self.requests = 0


    def solveQP(self,H,f,A,b,LB,UB,QPsolver):
        
    
        # persistent requests;
        # persistent errors;

        # if isempty(requests)
        #     requests    = 0;
        #     errors      = 0;
        # end
        
        # if nargin < 4 && nargin > 0 && strcmpi(varargin{1},'counts')
        #     varargout   = {requests,errors};
        #     return
        # end
        
        # Todo: update requests
        self.requests += 1
        if QPsolver == "gurobi":
            
            # H,f always exist
            # LB and UB always exist
            #  formulation of QP has no 1/2
            H = H/2

            nvar = len(f)
            # Create a new model
            m = gp.Model()
            vtype = [GRB.CONTINUOUS] * nvar
            
            # Add variables to model
            vars = []
            for j in range(nvar):
                vars.append(m.addVar(lb=LB[j], ub=UB[j], vtype=vtype[j]))
            x_vec = np.array(vars).reshape(nvar,1)

            if np.any(A != None) and np.any(b != None):
                Aeq = A
                beq = b
                # Populate A matrix
                expr = gp.LinExpr()
                Ax = Aeq @ x_vec
                expr += Ax[0,0]
                m.addLConstr(expr, GRB.GREATER_EQUAL, beq)
            else:
                #  no constraint A*x < b
                pass

            solution = np.zeros((nvar,1))

            # Populate objective: x.THx + f.T x
            obj = gp.QuadExpr()
            xTHx = x_vec.T @ H @ x_vec + f.T @ x_vec
            obj += xTHx[0,0]
            m.setObjective(obj)

            #  suppress output
            # m.Params.LogToConsole = 0
            m.Params.outputflag = 0

            m.optimize()
            x = m.getAttr('x', vars)
            for i in range(nvar):
                solution[i,0] = x[i]

            return solution

# # Create variables
    # x = m.addVars(nvar,1)
    # lst = []
    # for i in range(len(x)):
    #     lst.append(x[i,0])
    # x_vec = np.array(lst)
    # x_vec = x_vec.reshape(nvar,1)
    
    # # Set objective: x.THx + f.T x
    # obj = x_vec.T @ H @ x_vec + f.T @ x_vec
    # m.setObjective(obj[0][0])
    
    


    
    # # LB and UB always exist
    # m.addConstrs(x_vec[i][0] >= LB[i] for i in range(len(LB)))
    # m.addConstrs(x_vec[i][0] <= UB[i] for i in range(len(UB)))
    
    #  suppress output
    # m.Params.LogToConsole = 0
    # m.Params.outputflag = 0
    
    

    # result_lst = []
    # for v in m.getVars():
    #     result_lst.append(v.x)
    # result  = np.array([result_lst]).T