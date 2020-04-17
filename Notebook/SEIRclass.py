# SEIR model class definition
# Dr. Tirthajyoti Sarkar, Fremont, CA
# April 2020

import numpy as np
import matplotlib.pyplot as plt

class SEIR:
    def __init__(self,
                 init_vals=[1 - 1/1000, 1/1000, 0, 0], 
                 params_=[0.2,1.75,0.5,0.9]):
        """
        Initializes and sets the initial lists and parameters
        Arguments:
                init_vals: Fractions of population in the S, E, I, and R categories
                params_: Dynamical parameters - alpha, beta, gamma, and rho.
                Here the last parameter 'rho' models social distancing factor.
        """
        # Initial values
        self.s0 = init_vals[0]
        self.e0 = init_vals[1]
        self.i0 = init_vals[2]
        self.r0 = init_vals[3]
        # Lists
        self.s, self.e, self.i, self.r = [self.s0], [self.e0], [self.i0], [self.r0]
        # Dynamical parameters
        self.alpha = params_[0]
        self.beta = params_[1]
        self.gamma = params_[2]
        self.rho = params_[3]
        # All parameters together in a list
        self.params_ = [self.alpha,self.beta,self.gamma,self.rho]
        # All final values together in a list
        self.vals_ = [self.s[-1], self.e[-1], self.i[-1], self.r[-1]]
    
    def reinitialize(self,init_vals,verbose=False):
        """
        Re-initializes with new values
        """
        assert len(init_vals)==4,"Four initial values are expected"
        assert type(init_vals)==list, "Initial values are expected in a list"
        # Initial values
        self.s0 = init_vals[0]
        self.e0 = init_vals[1]
        self.i0 = init_vals[2]
        self.r0 = init_vals[3]
        
        if verbose:
            print("Initialized with the following values\n"+"-"*50)
            print("S0: ",self.s0)
            print("E0: ",self.e0)
            print("I0: ",self.i0)
            print("R0: ",self.r0)
    
    def set_params(self,params_,verbose=False):
        """
        Sets the dynamical parameters value
        """
        assert len(params_)==4,"Four parameter values are expected"
        assert type(params_)==list, "Parameter values are expected in a list"
        # Dynamical parameters
        self.alpha = params_[0]
        self.beta = params_[1]
        self.gamma = params_[2]
        self.rho = params_[3]
        self.params_ = [self.alpha,self.beta,self.gamma,self.rho]
        
        if verbose:
            print("Set the following parameter values\n"+"-"*50)
            print("alpha: ",self.alpha)
            print("beta: ",self.beta)
            print("gamma: ",self.gamma)
            print("rho: ",self.rho)
        
    def reset(self):
        """
        Resets the internal lists to zero-state
        """
        self.s, self.e, self.i, self.r = [self.s0], [self.e0], [self.i0], [self.r0]
    
    def run(self,t_max=100,dt=0.1,reset=True):
        """
        Runs the dynamical simulation
        Arguments:
                t_max: Maximum simulation time, e.g. 20 or 100 (can be thought of days)
                dt: Time step interval e.g. 0.1 or 0.02, a small value
                reset: A flag to reset the internal lists (restarts the simulation from initial values)
        """
        if reset:
            self.reset()
        # Time step array
        t = np.linspace(0, t_max, int(t_max/dt) + 1)
        # Temp lists
        S, E, I, R = self.s, self.e, self.i, self.r
        # Temp parameters
        alpha, beta, gamma, rho = self.alpha,self.beta,self.gamma,self.rho
        dt = t[1] - t[0]
        # Loop
        for _ in t[1:]:
            next_S = S[-1] - (rho*beta*S[-1]*I[-1])*dt
            next_E = E[-1] + (rho*beta*S[-1]*I[-1] - alpha*E[-1])*dt
            next_I = I[-1] + (alpha*E[-1] - gamma*I[-1])*dt
            next_R = R[-1] + (gamma*I[-1])*dt
            S.append(next_S)
            E.append(next_E)
            I.append(next_I)
            R.append(next_R)
        # Stack results
        result = np.stack([S, E, I, R]).T
        self.s, self.e, self.i, self.r = S, E, I, R
        # Update final values
        self.vals_ = [self.s[-1], self.e[-1], self.i[-1], self.r[-1]]
        
        return result
    
    def plot(self,results=None):
        """
        Plots the basic results
        """
        # Runs a simulation is no result is provided
        if results is None:
            results = self.run()
        # Plot
        plt.figure(figsize=(12,8))
        plt.plot(results,lw=3)
        plt.title('Basic SEIR Model',fontsize=18)
        plt.legend(['Susceptible', 'Exposed', 'Infected', 'Recovered'],
                   fontsize=15)
        plt.xlabel('Time Steps',fontsize=16)
        plt.ylabel('Fraction of Population',fontsize=16)
        plt.grid(True)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.show()
    
    def plot_var(
        self,
        var,
        var_name=None,
        show=True):
        """
        Plots the given variable
        Expect a list or Numpy array as the variable
        If var is None, plots the infected fraction
        """
        if var is None:
            var = self.i
        plt.figure(figsize=(12,8))
        plt.plot(var,lw=3,c='blue')
        plt.title('Basic SEIR Model',fontsize=18)
        if var_name is not None:
            plt.legend([var_name],fontsize=15)
        plt.xlabel('Time Steps',fontsize=16)
        plt.ylabel('Fraction of Population',fontsize=16)
        plt.grid(True)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        if show:
            plt.show()