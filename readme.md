# Overview

In February 2015, the City of New York created a new Tenant Harassment Prevention Taskforce to protect residents of rent stabilized homes. There are some 1 million rent stabilized units in the city, comprising of almost half of the rental housing stock [reference: http://furmancenter.org/research/publication/profile-of-rent-stabilized-units-and-tenants-in-new-york-city]. With the real estate market booming, city leadership was determined to take action against a small minority of landlords who engaged in predatory and illegal behavior to drive tenants out of their homes.

MODA helped the Taskforce focus inspection and enforcement resources where risk is highest, supporting a data-driven approach to standing up for tenants' rights.

## 1. Scoping

WHAT IS THE ANALYTICS QUESTION?

State law defines tenant harassment as a pattern of behavior that disturbs the comfort of rent-stabilized residents with intent to force their departure . Examples cited in court have included landlords shutting off heat and hot water during freezing weather, imposing extreme noise and dust from construction, or creating other unsanitary conditions. 

NYC has some of the strongest laws protecting renters in the country. However there is a legal loophole allowing units to become deregulated when tenants leave, if the rent surpasses a maximum threshold. This, along with high market rate rents, sets up a situation where there is clear financial incentive for landlords to force tenants out of their rent regulated apartments.  

The Taskforce, made up of city and state agencies including HPD, DOB, DOHMH, and DHCR, was charged with sending inspection team to apartments to issue violations where needed. In addition the NY AG’s office followed up with litigation procedures in cases where the teams saw direct evidence of harassment rising to the level of criminality. [reference: http://www1.nyc.gov/site/hpd/renters/thpt.page ]

The Taskforce visited units based on recommendations from elected officials and community groups. However they also wanted to add on a wider set of units that these sources may have missed. They turned to MODA to help identify buildings with possible tenant harassment based on information available in city data.

Because there was no city data set of tenant harassment, and because harassment and deregulation are so intimately linked, MODA redefined the analytics question from “What conditions are possible indicators of tenant harassment?” to “What conditions are possible indicators of rent regulated unit loss?”
  

## 2. Data

WHAT DATA IS REQUIRED?

Data on rent regulated apartments is not straightforward to obtain. DHCR is the state agency in charge of regulating these units. Unfortunately we could not get data directly from DHCR. But it turns out the City also has useful data to piece this together. DOF charges a $10 tax on every rent regulated unit. John Krauss was able to obtain this data from DOF and put them into a well-documented and useful format.  https://github.com/talos/nyc-stabilization-unit-counts
Understanding this data was key to running our analysis.

MODA's partners suggested several phenomena that may correlate with rent regulated unit loss, such as recently sold buildings, a history of tenant complaints, the presence of sudden bursts of construction activity, illegal construction, landlords taking tenants to court, and the size of the gap between regulated rent and potential market rent.

In addition to the rent stabilization count data from John Krauss, we also had access to:
•HPD Complaints and Violations
•DOB Complaints and Violations
•311 Complaints (for all agencies)
•DOB Construction Permits 
•DOF Sales
•DOF Rent Regulation Tax

## 3. Analysis

WHAT DATA ANALYSIS IS APPLICABLE?

We set out to test which hypothesized housing conditions preceded loss of rent regulated units. First we came up the hypothesized list of predictors based on our discussion with members of the Taskforce.

|  Predictor |  Data Used |
|:---|:---|
| Property Sales  | DOF Ownership data – when an owner name is updated  |
| Construction  | DOB Jobs filing, type alt 1-3, on multiple floors  |
| Illegal Construction  | 311 Service Requests, DOB Complaints for illegal work  |
| Complaints from residents  | 311 Service Requests  |

 
The City's 311 service offers an extensive store of data about problems or requests for city services originating with residents. Because there are more than two thousand different complaint types under 311, we grouped these into categories related to tenant harassment.

| Category | Definition |
|:---|:---|
|Air Quality - NonConstruction|	DEP air quality complaints not directly related to construction|
|Asbestos| DEP/DOHMH asbestos complaints|
|Dust – Construction DEP|	Dust from construction (outdoor) routed to DEP|
|Dust – Construction DOHMH|	Dust from construction (indoor) routed to DOHMH|
|Construction|	Complaint area containing 'construction'|
|DOB Illegal Work|	DOB complaint containing: illegal, unsafe, safety, or permit|
|DOB| 	Any other DOB complaint|
|Dirty Conditions|	Includes DSNY/DOHMH rodent, mold, unsanitary, standing water, vector, sanitation condition, dirty conditions|
|HPD - No Services|	HPD Heat/Hot water, electric, gas, refrigerator|
|HPD|	Any other HPD complaint|
|Hazardous Materials|	DEP hazardous materials|
|Other|	Everything not included in other categories. These are complaints expected to be tangentially related to tenant harassment.|
|NA|	Not Applicable Agencies:  DOE, TLC, EDC, DCA, DOITT |


All the predictors shared a unique identifier with the DOF rent stabilized data, so we were able to merge these together and then test for which predictors were more likely to be associated with unit loss. We decided to concentrate on whether or not a predictor, like a 311 complaint, was present. But not how many times someone complained. This was done to not over emphasise places where someone is 

The Risk Ratio is a comparison of the probability of unit loss in buildings where a predictor was present in the previous year, with the baseline probability of unit loss for all buildings across the city. The findings of this analysis showed which predictors were associated with unit loss. We used the risk ratio because it is straightforward to explain and understand. More complicated multivariate analysis may be possible (although limited by the amount of data we have), but then we loose the straignforward explainability without gaining much in predictability. We steered away from overengineering the analysis, especially since our ultimate goal is identifying where tenant harasment is happening while the data we have to work with is on unit loss.

As well as confirming the importance of key indicators such as recent sales followed by construction activity, the analysis also brought into focus several additional indicators that could have been overlooked. Buildings with recent asbestos complaints, for example, were five times more likely to experience rent stabilized unit loss compared with the average rent stabilized building. 

## 4. Pilot

HOW CAN THE ANALYSIS IMPROVE THE OPERATION?

Once we identified the predictors associated with unit loss, we compiled a list of buildings exhibiting one or more of them in the past six months. We worked with the unit at HPD in charge of selecting addresses for the Taskforce. They based most of their inspections on word of mouth recommendations, but also wanted to send the taskforce to other places in that same vicinity. This allowed for more efficient use of the inspection teams’ time. For that they were able to sort the list by neighborhood and send the inspection teams to those addresses.

EVALUATION

MODA received anecdotal evidence that the model was working and feeding the inspection teams places that were useful. However, because MODA did not have access to the results of the Taskforce inspections (e.g. places were visited, types of violations issued, other follow ups), we do not have a quantitative way of assessing the model or making changes to it.

## 5. Handoff

IS THE MODEL SUSTAINABLE?

MODA sends an updated list of buildings to the Taskforce every two to three months. A citywide data sharing mechanism would allow the Taskforce to access those lists as they needed. Once that is in place the Taskforce would engage MODA to revisit the model and run further analysis, but would not be dependent on MODA for data pulls.

## Summary:

Prior to this project, the Tenant Harassment Prevention Taskforce selected addresses for inspections and follow-up actions based on recommendations and professional judgment. The model added value by bringing datasets together to model behavior associated with a carefully defined target variable. The list has helped inspectors, when in a specific neighborhood, select additional addresses to visit. While expert judgment has remained central to countering predatory landlords, the analysis has helped identify key factors that correlate strongly with rent stabilized unit loss, bringing high-risk complaints to the front of the queue for enforcement action.
