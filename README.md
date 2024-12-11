## Literature Review

### Attributes use for Diabetes Prediction

- [Optimization of diabetes prediction methods based on combinatorial balancing algorithm](https://www.nature.com/articles/s41387-024-00324-z#Tab1) use Gender, Age, Hypertension, Heart_disease, Smoking_history, BMI, Glycated Hemoglobin Level, Blood Glucose Level

- [Diabetes Prediction using Machine Learning Algorithms](https://www.sciencedirect.com/science/article/pii/S1877050920300557) use Glucose Level, Blood Pressure, Skin Thickness(mm), Insulin, BMI, Age, Job Type(Office-work/Fieldwork/Machine-work) 


## EDA 

### Demographic Analysis

<!-- #### Diabetes v/s Gender -->

|Gender |Percentage |
|------|------|
|Male| 48.06|
|Female|51.94|

#### Age 

Older individuals are more commonly affected by diabetes, while younger individuals tend to have a lower risk.

![Age](images/age_distribution.png)

In the provided dataset, the distribution of diabetic cases among males and females across different age groups is similar.


![Age and Gender](images/age_gender_distribution.png)

### Weight History

#### BMI (Relative)

| Statistic | Diabetes            | Non Diabetes |
|-----------|---------------------|--------------|
| Mean      | 0.045443            | 0.039753     |
| Std       | 0.010822            | 0.009509     |
| Min       | 0.017637            | 0.016039     |
| 25%       | 0.037870            | 0.033287     |
| 50%       | 0.043945            | 0.037870     |
| 75%       | 0.050728            | 0.044343     |
| Max       | 0.112500            | 0.109261     |

![BMI and Age](images/scatter_age_bmi.png) 

The distribution of Age v/s BMI for diabetes patient is almost similar for both gender

![Gender, BMI and Age](images/plot_age_bmi_gender_diabetes.png) 



#### Weight Change (Interquartile Range)

- For Diabetes, Weight Change - Q1: -15.0 and Q3: 0.0 
- For Non-Diabetes, Weight Change - Q1: -5.0 and Q3: 5.0

#### Tried to loss Weight

- For Diabetes, Tried to Lose Weight People Percentage: 48.54%
- For Non-Diabetes, Tried to Lose Weight People Percentage: 44.71%

It's almost equal percentage, not a good factor

![Tried to lose weight plot](images/tried_lose_weight.png)

### Occupation

#### Work Experience

People who are not working at a job or business are more prone to diabetes

![Work Experience plot](images/work_experience.png)

**Working at Job or Business** : Diabetes is more commonly observed among older individuals in this group.

**Not Working at Job or Business** : This group predominantly consists of older individuals. The average age is similar for both diabetic and non-diabetic individuals, but the interquartile range of age for diabetic patients is narrow, falling between 62 and 75 years. Both male and female who are suffering from diabetes have similar average age.

![Age Work Experience plot](images/age_work_experience.png)

![Gender Age Work Experience plot](images/age_work_experience_gender.png)

#### Working Hours

Woking hours does not have much influence.
- Mean working hours of a person having diabetes = 38.465 hrs
- Mean working hours of a person not having diabetes = 38.667 hrs
- Average working days for people with diabetes in a week: 4.83
- Average working days for people without diabetes in a week: 4.81

![Working Hours plot](images/working_hours.png)


#### Reasons of not working last week 

- Percentage of people with diabetes who are not working because of health issues:  31.32%

- Percentage of people without diabetes who are not working because of health issues:  16.84%

![Reasons for not working plot](images/reason_not_working.png)


### Blood Pressure and Cholesterol

 - 72.041% of individuals with diabetes have been informed about hypertension.
 - Only 28.44% of individuals with no diabetes have been informed about hypertension.

 ![Ever Told Hypertension](images/ever_told_high_bp.png)

 - 70.8% of individuals with diabetes have been informed about cholesterol.
 - Only 30.58% of individuals with no diabetes have been informed about hypertension.

 ![Ever Told Cholesterol](images/ever_told_high_cholesterol.png)

#### Blood pressure medication

- Proportion of People with diabetes who are taking blood pressure medication: 0.9094
- Proportion of People without diabetes who are taking blood pressure medication: 0.7932

#### Do they Smoke now ?     

|           |       Diabetic           |     Non-Diabetic       |
|-----------|---------------------|--------------|
|  Every day |0.2514           | 0.3067     |
|  Some days	 | 0.0646         | 0.0757     |
|  Not at all		 | 0.6839         | 0.6175     |

- Smoking data have a lot of missing values.

### Hearing Condition

- Diabetic Patients suffer from hearing problems more as compare to healthy patients as depicted in the figure below and also in article [link](https://www.cdc.gov/diabetes/diabetes-complications/diabetes-and-hearing-loss.html#:~:text=Low%20blood%20sugar%20over%20time,same%20age%20who%20don't.).

 ![General Hearing Condition](images/hearing_condition.png)

 ### General Health Condition

 -  The general health condition of most of the diabetic patients is not so good when we compare it with non-diabetic persons.

   ![General Health Condition](images/general_health.png)
