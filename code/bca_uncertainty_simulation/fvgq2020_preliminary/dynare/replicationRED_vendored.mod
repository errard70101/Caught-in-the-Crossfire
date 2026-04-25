// Code to replicate RED Paper "Uncertainty Shocks and Business Cycle Research"
// JFV -- PaGq
// November 2019

// Set to 1 to replicate results with higher phi
// 0 = baseline
@#define higherphi = 0

// NOTE: add the pruning library from the Restud paper by Andreasen, Fernandez-Villaverde, and Rubio-Ramirez.
addpath(genpath('/Users/various/Dynare44Pruning/simAndMoments3order')) ;

var ce cw ivst q k labor y cspt phi utilt delt deltp demt lambdat At sigAt sigdt thetat siget ; 
varexo ethet eA ed uA ud ue ;

parameters beta ifrac alpha delt0 delt1 delt2 ssPhi theta rho eta gss rhothet rhoA rhod sigA sigd sige rhosigA rhosigd rhosige metaA metad metae;


beta = 0.994;
ifrac = 0.06;
alpha = 0.36;
delt0 = 0.01625;
@#if higherphi == 0
ssPhi = 0.09539948379;
delt1 = 0.01309569021;
delt2 = 0.33*delt1;
@#else
ssPhi = 0.2 ;   
delt1 = 0.02052077068;
delt2 = 0.33*delt1;
@#endif
theta = ssPhi; 
rho = 2;
eta = 1.524829433;
gss = 1.00;


rhothet = 0.95;
rhoA  = 0.95 ; // frontiers
sigA  = log(0.007) ; // from frontiers of BC
sige  = log(0.033/4) ; // GJ in QE
rhod  = 0.95 ;
sigd  = log(0.13/4) ; // FGR
rhosigA = 0.75 ; // midrange of persistence in FGR, JE 2015
rhosigd = 0.75 ;
rhosige = 0.75 ;
metaA =  (log(2)/(1-rhosigA^2)^0.5) ; 0.01 ;
metad =  (log(2)/(1-rhosigd^2)^0.5) ;0.2 ;
metae =  (log(2)/(1-rhosige^2)^0.5) ;0.05 ;

// Model definition
model;

((ce))^(-rho) = (1 + ((q)-1)/(1-thetat*(q)))*((cw))^(-rho)*(1-(labor))^(eta*(1-rho));

eta*(cw)/(1-(labor)) = (1-alpha)*((y))/((1-ifrac)*(labor));
// labor = (0.3546099291) ;

(q) = beta*demt(1)/demt*(gss*(cw(+1))/(cw))^(-rho)*((1-(labor(+1)))/(1-(labor)))^(eta*(1-rho))
        *(alpha*((y(+1)))/(utilt(+1)*k) + (q(+1))*(1-delt) 
        + ifrac*(((q(+1))-1)/(1-thetat(+1)*(q(+1))))*( alpha*((y(+1)))/(utilt(+1)*k) + (q(+1))*(1-delt)*(phi(+1)) ) );

(ce) + (1 - thetat*(q))*(ivst) = alpha*(y) + (q)*(phi)*(1-delt)*(k(-1)) ;

(y) = (At)*((utilt*k(-1)))^alpha*((1-ifrac)*(labor))^(1-alpha);

(y) = ifrac*(ce) + (1 - ifrac)*(cw) + ifrac*(ivst);

(k) = (1 - delt)*(k(-1)) + ifrac*(ivst);

phi = ssPhi ;

// Level shocks

thetat = (1-rhothet)*(theta) + rhothet*thetat(-1) + exp(siget)*ethet;

At  = (1 - rhoA) + rhoA*At(-1) + exp(sigAt)*eA ;

demt = 1 - rhod + rhod*demt(-1) + exp(sigdt)*ed ;

// Volatility shocks

(sigAt) = (1-rhosigA)*(sigA) + rhosigA*(sigAt(-1)) + (1-rhosigA^2)^(0.5)*metaA*uA ;

(sigdt) = (1-rhosigd)*(sigd) + rhosigd*(sigdt(-1)) + (1-rhosigd^2)^(0.5)*metad*ud ;

(siget) = (1-rhosige)*(sige) + rhosige*(siget(-1)) + (1-rhosige^2)^(0.5)*metae*ue ;

(cspt) = ifrac*(ce) + (1-ifrac)*(cw);

alpha*(y)/(utilt*k(-1)) - (q)*deltp + ((q)-1)/(1-thetat*(q))*ifrac*(alpha*(y)/(utilt*k(-1)) - phi*(q)*deltp) = 0 ;

delt = delt0 + delt1*(utilt - 1) + delt2/2*(utilt - 1)^2 ;

deltp = delt1 + delt2*(utilt - 1) ;

(lambdat) = ((q) - 1)/(1 - (q)*theta) ;

end;

shocks;
var ethet = 1 ;
var eA = 1 ;
var ed = 1 ;
var uA = 1 ;
var ud = 1 ;
var ue = 1 ;
end;

initval;
@#if higherphi == 0
ce = (0.5913719745);
cw = (1.101401063);
ivst = (5.087186128);
k = (18.78345647);
q = (2.26297);
y = (1.422989127);
labor = (0.3546099291);
phi = (ssPhi);
cspt = (1.070799318);
utilt = 1 ;
delt = delt0 ;
deltp = delt1 ;
demt = 1 ;
lambdat = (((1.568268059) - 1)/(1-(1.568268059)*theta)) ;
At   = 1 ;
thetat = theta ;
sigAt = (sigA) ;
sigdt = (sigd) ;
siget = (sige) ;
@#else
ce = (0.8202039838);
cw = (1.250189404);
ivst = (7.08561785087176);
k = (26.16228137);
q = (1.113859944);
y = (1.649527351);
labor = (0.3707267006);
phi = (ssPhi);
cspt = (1.224390278);
utilt = 1 ;
delt = delt0 ;
deltp = delt1 ;
demt = 1 ;
lambdat = (((1.113859944) - 1)/(1-(1.113859944)*theta)) ;
At   = 1 ;
thetat = theta ;
sigAt = (sigA) ;
sigdt = (sigd) ;
siget = (sige) ;
@#endif
end;

resid(1) ;

steady(solve_algo=3);

//---------------------------------------------------------------------
// 5. Run Dynare with pruning
//---------------------------------------------------------------------
// Default step: a first-order approximation needed for RunDynarePruning
stoch_simul(order = 1, nomoments, noprint, irf = 0) ;
f_11 = [oo_.dr.ghx oo_.dr.ghu];

// The standard Dynare command for your model
stoch_simul(order = 3, irf = 0);

// Options for running the pruning codes
optPruning.numSim         = 1;                    
optPruning.seedNum        = 1;  
optPruning.IRFlength      = 41;
optPruning.computeIRF     = 1;
optPruning.plotIRF        = 0;
optPruning.computeMoments = 1;
optPruning.orderApp       = options_.order;   
optPruning.shockSize      = 1 ;
tic                                   
outDynare = RunDynarePruning(optPruning,oo_,M_,f_11);
toc

// To see the applied options
outDynare.opt
locy = [10 3 2 9 8 6 12] ;
// shocks order
// ethet eA ed uA ud ue

// Volatility financial sector
locx = 6 ;
locv = 5 ;

//---------------------------------------------------------------------

yirf = [] ;
for ix = 1:length(locy)
    yirf = [yirf;100*outDynare.IRFy(locy(ix),1:end-1,3,locx)/outDynare.gSteadyState(locy(ix))] ;
end
// IRFs are in matrix yirf
// Order in which_
yirf = [yirf;outDynare.IRFv(locv,2:end,3,locx)] ;
which_ = strvcat('output','consumption','investment','labor','price of capital','lambda','utilt','shock') ;


// Volatility Preference 
locx = 5 ;
locv = 4 ;
//---------------------------------------------------------------------

yirf = [] ;
for ix = 1:length(locy)
    yirf = [yirf;100*outDynare.IRFy(locy(ix),1:end-1,3,locx)/outDynare.gSteadyState(locy(ix))] ;
end
yirf = [yirf;outDynare.IRFv(locv,2:end,3,locx)] ;
which_ = strvcat('output','consumption','investment','labor','price of capital','lambda','utilt','shock') ;
endogz_ = which_ ;


// Volatility Productivity
locx = 4 ;
locv = 3 ;
//---------------------------------------------------------------------

yirf = [] ;
for ix = 1:length(locy)
    yirf = [yirf;100*outDynare.IRFy(locy(ix),1:end-1,3,locx)/outDynare.gSteadyState(locy(ix))] ;
end
yirf = [yirf;outDynare.IRFv(locv,2:end,3,locx)] ;
which_ = strvcat('output','consumption','investment','labor','price of capital','lambda','utilt','shock') ;


// level shock financial sector
locx = 1 ;
locv = 7 ;
//---------------------------------------------------------------------

yirf = [] ;
for ix = 1:length(locy)
    yirf = [yirf;100*outDynare.IRFy(locy(ix),1:end-1,3,locx)/outDynare.gSteadyState(locy(ix))] ;
end
yirf = [yirf;outDynare.IRFv(locv,2:end,3,locx)] ;
which_ = strvcat('output','consumption','investment','labor','price of capital','lambda','utilt','shock') ;

