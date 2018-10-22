
## Encoding Categorical Values in Python



```python
import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelBinarizer, LabelEncoder

import category_encoders as ce
```


```python
headers = ["symboling", "normalized_losses", "make", "fuel_type", "aspiration", "num_doors", "body_style",
           "drive_wheels", "engine_location", "wheel_base", "length", "width", "height", "curb_weight",
           "engine_type", "num_cylinders", "engine_size", "fuel_system", "bore", "stroke", 
           "compression_ratio", "horsepower", "peak_rpm", "city_mpg", "highway_mpg", "price"]
```


```python
df = pd.read_csv("http://mlr.cs.umass.edu/ml/machine-learning-databases/autos/imports-85.data",
                 header=None, names=headers, na_values="?" )
```


```python
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>symboling</th>
      <th>normalized_losses</th>
      <th>make</th>
      <th>fuel_type</th>
      <th>aspiration</th>
      <th>num_doors</th>
      <th>body_style</th>
      <th>drive_wheels</th>
      <th>engine_location</th>
      <th>wheel_base</th>
      <th>...</th>
      <th>engine_size</th>
      <th>fuel_system</th>
      <th>bore</th>
      <th>stroke</th>
      <th>compression_ratio</th>
      <th>horsepower</th>
      <th>peak_rpm</th>
      <th>city_mpg</th>
      <th>highway_mpg</th>
      <th>price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3</td>
      <td>NaN</td>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>convertible</td>
      <td>rwd</td>
      <td>front</td>
      <td>88.6</td>
      <td>...</td>
      <td>130</td>
      <td>mpfi</td>
      <td>3.47</td>
      <td>2.68</td>
      <td>9</td>
      <td>111</td>
      <td>5000</td>
      <td>21</td>
      <td>27</td>
      <td>13495</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3</td>
      <td>NaN</td>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>convertible</td>
      <td>rwd</td>
      <td>front</td>
      <td>88.6</td>
      <td>...</td>
      <td>130</td>
      <td>mpfi</td>
      <td>3.47</td>
      <td>2.68</td>
      <td>9</td>
      <td>111</td>
      <td>5000</td>
      <td>21</td>
      <td>27</td>
      <td>16500</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>NaN</td>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>hatchback</td>
      <td>rwd</td>
      <td>front</td>
      <td>94.5</td>
      <td>...</td>
      <td>152</td>
      <td>mpfi</td>
      <td>2.68</td>
      <td>3.47</td>
      <td>9</td>
      <td>154</td>
      <td>5000</td>
      <td>19</td>
      <td>26</td>
      <td>16500</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2</td>
      <td>164</td>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>four</td>
      <td>sedan</td>
      <td>fwd</td>
      <td>front</td>
      <td>99.8</td>
      <td>...</td>
      <td>109</td>
      <td>mpfi</td>
      <td>3.19</td>
      <td>3.40</td>
      <td>10</td>
      <td>102</td>
      <td>5500</td>
      <td>24</td>
      <td>30</td>
      <td>13950</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2</td>
      <td>164</td>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>four</td>
      <td>sedan</td>
      <td>4wd</td>
      <td>front</td>
      <td>99.4</td>
      <td>...</td>
      <td>136</td>
      <td>mpfi</td>
      <td>3.19</td>
      <td>3.40</td>
      <td>8</td>
      <td>115</td>
      <td>5500</td>
      <td>18</td>
      <td>22</td>
      <td>17450</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 26 columns</p>
</div>



Look at the data types contained in the dataframe


```python
df.dtypes
```




    symboling              int64
    normalized_losses    float64
    make                  object
    fuel_type             object
    aspiration            object
    num_doors             object
    body_style            object
    drive_wheels          object
    engine_location       object
    wheel_base           float64
    length               float64
    width                float64
    height               float64
    curb_weight            int64
    engine_type           object
    num_cylinders         object
    engine_size            int64
    fuel_system           object
    bore                 float64
    stroke               float64
    compression_ratio    float64
    horsepower           float64
    peak_rpm             float64
    city_mpg               int64
    highway_mpg            int64
    price                float64
    dtype: object



Create a copy of the data with only the object columns.


```python
obj_df = df.select_dtypes(include=['object']).copy()
```


```python
obj_df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>make</th>
      <th>fuel_type</th>
      <th>aspiration</th>
      <th>num_doors</th>
      <th>body_style</th>
      <th>drive_wheels</th>
      <th>engine_location</th>
      <th>engine_type</th>
      <th>num_cylinders</th>
      <th>fuel_system</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>convertible</td>
      <td>rwd</td>
      <td>front</td>
      <td>dohc</td>
      <td>four</td>
      <td>mpfi</td>
    </tr>
    <tr>
      <th>1</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>convertible</td>
      <td>rwd</td>
      <td>front</td>
      <td>dohc</td>
      <td>four</td>
      <td>mpfi</td>
    </tr>
    <tr>
      <th>2</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>hatchback</td>
      <td>rwd</td>
      <td>front</td>
      <td>ohcv</td>
      <td>six</td>
      <td>mpfi</td>
    </tr>
    <tr>
      <th>3</th>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>four</td>
      <td>sedan</td>
      <td>fwd</td>
      <td>front</td>
      <td>ohc</td>
      <td>four</td>
      <td>mpfi</td>
    </tr>
    <tr>
      <th>4</th>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>four</td>
      <td>sedan</td>
      <td>4wd</td>
      <td>front</td>
      <td>ohc</td>
      <td>five</td>
      <td>mpfi</td>
    </tr>
  </tbody>
</table>
</div>



Check for null values in the data


```python
obj_df[obj_df.isnull().any(axis=1)]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>make</th>
      <th>fuel_type</th>
      <th>aspiration</th>
      <th>num_doors</th>
      <th>body_style</th>
      <th>drive_wheels</th>
      <th>engine_location</th>
      <th>engine_type</th>
      <th>num_cylinders</th>
      <th>fuel_system</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>27</th>
      <td>dodge</td>
      <td>gas</td>
      <td>turbo</td>
      <td>NaN</td>
      <td>sedan</td>
      <td>fwd</td>
      <td>front</td>
      <td>ohc</td>
      <td>four</td>
      <td>mpfi</td>
    </tr>
    <tr>
      <th>63</th>
      <td>mazda</td>
      <td>diesel</td>
      <td>std</td>
      <td>NaN</td>
      <td>sedan</td>
      <td>fwd</td>
      <td>front</td>
      <td>ohc</td>
      <td>four</td>
      <td>idi</td>
    </tr>
  </tbody>
</table>
</div>



Since the num_doors column contains the null values, look at what values are current options


```python
obj_df['num_doors']
```




    0       two
    1       two
    2       two
    3      four
    4      four
    5       two
    6      four
    7      four
    8      four
    9       two
    10      two
    11     four
    12      two
    13     four
    14     four
    15     four
    16      two
    17     four
    18      two
    19      two
    20     four
    21      two
    22      two
    23      two
    24     four
    25     four
    26     four
    27      NaN
    28     four
    29      two
           ... 
    175    four
    176    four
    177    four
    178     two
    179     two
    180    four
    181    four
    182     two
    183     two
    184    four
    185    four
    186    four
    187    four
    188    four
    189     two
    190     two
    191    four
    192    four
    193    four
    194    four
    195    four
    196    four
    197    four
    198    four
    199    four
    200    four
    201    four
    202    four
    203    four
    204    four
    Name: num_doors, dtype: object




```python
obj_df["num_doors"].value_counts()
```




    four    114
    two      89
    Name: num_doors, dtype: int64



We will fill in the doors value with the most common element - four.


```python
obj_df = obj_df.fillna({"num_doors": "four"})
```


```python
obj_df[obj_df.isnull().any(axis=1)]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>make</th>
      <th>fuel_type</th>
      <th>aspiration</th>
      <th>num_doors</th>
      <th>body_style</th>
      <th>drive_wheels</th>
      <th>engine_location</th>
      <th>engine_type</th>
      <th>num_cylinders</th>
      <th>fuel_system</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>



# Encoding values using pandas

## Convert the num_cylinders and num_doors values to numbers


```python
obj_df["num_cylinders"].value_counts()
```




    four      159
    six        24
    five       11
    eight       5
    two         4
    three       1
    twelve      1
    Name: num_cylinders, dtype: int64




```python
cleanup_nums = {"num_doors":     {"four": 4, "two": 2},
                "num_cylinders": {"four": 4, "six": 6, "five": 5, "eight": 8,
                                  "two": 2, "twelve": 12, "three":3 }}
```


```python
obj_df.replace(cleanup_nums, inplace=True)
```


```python
obj_df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>make</th>
      <th>fuel_type</th>
      <th>aspiration</th>
      <th>num_doors</th>
      <th>body_style</th>
      <th>drive_wheels</th>
      <th>engine_location</th>
      <th>engine_type</th>
      <th>num_cylinders</th>
      <th>fuel_system</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>2</td>
      <td>convertible</td>
      <td>rwd</td>
      <td>front</td>
      <td>dohc</td>
      <td>4</td>
      <td>mpfi</td>
    </tr>
    <tr>
      <th>1</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>2</td>
      <td>convertible</td>
      <td>rwd</td>
      <td>front</td>
      <td>dohc</td>
      <td>4</td>
      <td>mpfi</td>
    </tr>
    <tr>
      <th>2</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>2</td>
      <td>hatchback</td>
      <td>rwd</td>
      <td>front</td>
      <td>ohcv</td>
      <td>6</td>
      <td>mpfi</td>
    </tr>
    <tr>
      <th>3</th>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>4</td>
      <td>sedan</td>
      <td>fwd</td>
      <td>front</td>
      <td>ohc</td>
      <td>4</td>
      <td>mpfi</td>
    </tr>
    <tr>
      <th>4</th>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>4</td>
      <td>sedan</td>
      <td>4wd</td>
      <td>front</td>
      <td>ohc</td>
      <td>5</td>
      <td>mpfi</td>
    </tr>
  </tbody>
</table>
</div>


Check the data types to make sure they are coming through as numbers

```python
obj_df.dtypes
```




    make               object
    fuel_type          object
    aspiration         object
    num_doors           int64
    body_style         object
    drive_wheels       object
    engine_location    object
    engine_type        object
    num_cylinders       int64
    fuel_system        object
    dtype: object



One approach to encoding labels is to convert the values to a pandas category


```python
obj_df["body_style"].value_counts()
```




    sedan          96
    hatchback      70
    wagon          25
    hardtop         8
    convertible     6
    Name: body_style, dtype: int64




```python
obj_df["body_style"] = obj_df["body_style"].astype('category')
```


```python
obj_df.dtypes
```




    make                 object
    fuel_type            object
    aspiration           object
    num_doors             int64
    body_style         category
    drive_wheels         object
    engine_location      object
    engine_type          object
    num_cylinders         int64
    fuel_system          object
    dtype: object



We can assign the category codes to a new column so we have a clean numeric representation


```python
obj_df['fuel_type'].cat.codes
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-29-0382ac16f757> in <module>()
    ----> 1 obj_df['fuel_type'].cat.codes
    

    /usr/local/lib/python3.5/dist-packages/pandas/core/generic.py in __getattr__(self, name)
       2353                 or name in self._metadata
       2354                 or name in self._accessors):
    -> 2355             return object.__getattribute__(self, name)
       2356         else:
       2357             if name in self._info_axis:


    /usr/local/lib/python3.5/dist-packages/pandas/core/base.py in __get__(self, instance, owner)
        210             # this ensures that Series.str.<method> is well defined
        211             return self.accessor_cls
    --> 212         return self.construct_accessor(instance)
        213 
        214     def __set__(self, instance, value):


    /usr/local/lib/python3.5/dist-packages/pandas/core/series.py in _make_cat_accessor(self)
       2696     def _make_cat_accessor(self):
       2697         if not is_categorical_dtype(self.dtype):
    -> 2698             raise AttributeError("Can only use .cat accessor with a "
       2699                                  "'category' dtype")
       2700         return CategoricalAccessor(self.values, self.index)


    AttributeError: Can only use .cat accessor with a 'category' dtype



```python
obj_df["body_style_cat"] = obj_df["body_style"].cat.codes
```


```python
obj_df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>make</th>
      <th>fuel_type</th>
      <th>aspiration</th>
      <th>num_doors</th>
      <th>body_style</th>
      <th>drive_wheels</th>
      <th>engine_location</th>
      <th>engine_type</th>
      <th>num_cylinders</th>
      <th>fuel_system</th>
      <th>body_style_cat</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>2</td>
      <td>convertible</td>
      <td>rwd</td>
      <td>front</td>
      <td>dohc</td>
      <td>4</td>
      <td>mpfi</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>2</td>
      <td>convertible</td>
      <td>rwd</td>
      <td>front</td>
      <td>dohc</td>
      <td>4</td>
      <td>mpfi</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>2</td>
      <td>hatchback</td>
      <td>rwd</td>
      <td>front</td>
      <td>ohcv</td>
      <td>6</td>
      <td>mpfi</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>4</td>
      <td>sedan</td>
      <td>fwd</td>
      <td>front</td>
      <td>ohc</td>
      <td>4</td>
      <td>mpfi</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>4</td>
      <td>sedan</td>
      <td>4wd</td>
      <td>front</td>
      <td>ohc</td>
      <td>5</td>
      <td>mpfi</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>




```python
obj_df.dtypes
```




    make                 object
    fuel_type            object
    aspiration           object
    num_doors             int64
    body_style         category
    drive_wheels         object
    engine_location      object
    engine_type          object
    num_cylinders         int64
    fuel_system          object
    body_style_cat         int8
    dtype: object



## In order to do one hot encoding, use pandas get_dummies


```python
pd.get_dummies(obj_df, columns=["drive_wheels"]).head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>make</th>
      <th>fuel_type</th>
      <th>aspiration</th>
      <th>num_doors</th>
      <th>body_style</th>
      <th>engine_location</th>
      <th>engine_type</th>
      <th>num_cylinders</th>
      <th>fuel_system</th>
      <th>body_style_cat</th>
      <th>drive_wheels_4wd</th>
      <th>drive_wheels_fwd</th>
      <th>drive_wheels_rwd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>2</td>
      <td>convertible</td>
      <td>front</td>
      <td>dohc</td>
      <td>4</td>
      <td>mpfi</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>2</td>
      <td>convertible</td>
      <td>front</td>
      <td>dohc</td>
      <td>4</td>
      <td>mpfi</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>2</td>
      <td>hatchback</td>
      <td>front</td>
      <td>ohcv</td>
      <td>6</td>
      <td>mpfi</td>
      <td>2</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>4</td>
      <td>sedan</td>
      <td>front</td>
      <td>ohc</td>
      <td>4</td>
      <td>mpfi</td>
      <td>3</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>4</td>
      <td>sedan</td>
      <td>front</td>
      <td>ohc</td>
      <td>5</td>
      <td>mpfi</td>
      <td>3</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>



### get_dummiers has options for selecting the columns and adding prefixes to make the resulting data easier to understand.


```python
pd.get_dummies(obj_df, columns=["body_style", "drive_wheels"], prefix=["body", "drive"]).head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>make</th>
      <th>fuel_type</th>
      <th>aspiration</th>
      <th>num_doors</th>
      <th>engine_location</th>
      <th>engine_type</th>
      <th>num_cylinders</th>
      <th>fuel_system</th>
      <th>body_style_cat</th>
      <th>body_convertible</th>
      <th>body_hardtop</th>
      <th>body_hatchback</th>
      <th>body_sedan</th>
      <th>body_wagon</th>
      <th>drive_4wd</th>
      <th>drive_fwd</th>
      <th>drive_rwd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>2</td>
      <td>front</td>
      <td>dohc</td>
      <td>4</td>
      <td>mpfi</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>2</td>
      <td>front</td>
      <td>dohc</td>
      <td>4</td>
      <td>mpfi</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>2</td>
      <td>front</td>
      <td>ohcv</td>
      <td>6</td>
      <td>mpfi</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>4</td>
      <td>front</td>
      <td>ohc</td>
      <td>4</td>
      <td>mpfi</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>4</td>
      <td>front</td>
      <td>ohc</td>
      <td>5</td>
      <td>mpfi</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



## Another approach to encoding values is to select an attribute and convert it to True or False.


```python
obj_df["engine_type"].value_counts()
```




    ohc      148
    ohcf      15
    ohcv      13
    dohc      12
    l         12
    rotor      4
    dohcv      1
    Name: engine_type, dtype: int64



## Use np.where and the str accessor to do this in one efficient line


```python
obj_df["OHC_Code"] = np.where(obj_df["engine_type"].str.contains("ohc"), 1, 0)
```


```python
obj_df[["make", "engine_type", "OHC_Code"]].head(20)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>make</th>
      <th>engine_type</th>
      <th>OHC_Code</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>alfa-romero</td>
      <td>dohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>alfa-romero</td>
      <td>dohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>alfa-romero</td>
      <td>ohcv</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>audi</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>audi</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>audi</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>audi</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>audi</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>audi</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>audi</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>10</th>
      <td>bmw</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>11</th>
      <td>bmw</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12</th>
      <td>bmw</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>13</th>
      <td>bmw</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>14</th>
      <td>bmw</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>15</th>
      <td>bmw</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>16</th>
      <td>bmw</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>bmw</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
    <tr>
      <th>18</th>
      <td>chevrolet</td>
      <td>l</td>
      <td>0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>chevrolet</td>
      <td>ohc</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



# Encoding Values Using Scitkit-learn

### Instantiate the LabelEncoder


```python
lb_make = LabelEncoder()
```


```python
obj_df["make_code"] = lb_make.fit_transform(obj_df["make"])
```


```python
obj_df[["make", "make_code"]].head(11)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>make</th>
      <th>make_code</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>alfa-romero</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>alfa-romero</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>alfa-romero</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>audi</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>audi</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>audi</td>
      <td>1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>audi</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>audi</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>audi</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>audi</td>
      <td>1</td>
    </tr>
    <tr>
      <th>10</th>
      <td>bmw</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>



## To accomplish something similar to pandas get_dummies, use `LabelBinarizer`


```python
lb_style = LabelBinarizer()
lb_results = lb_style.fit_transform(obj_df["body_style"])
```

The results are an array that needs to be converted to a DataFrame


```python
lb_style.classes_
```




    array(['convertible', 'hardtop', 'hatchback', 'sedan', 'wagon'],
          dtype='<U11')




```python
lb_results
```




    array([[1, 0, 0, 0, 0],
           [1, 0, 0, 0, 0],
           [0, 0, 1, 0, 0],
           ...,
           [0, 0, 0, 1, 0],
           [0, 0, 0, 1, 0],
           [0, 0, 0, 1, 0]])




```python
pd.DataFrame(lb_results, columns=lb_style.classes_).head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>convertible</th>
      <th>hardtop</th>
      <th>hatchback</th>
      <th>sedan</th>
      <th>wagon</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



# Advanced Encoding
[category_encoder](http://contrib.scikit-learn.org/categorical-encoding/) library


```python
# Get a new clean dataframe
obj_df = df.select_dtypes(include=['object']).copy()
```


```python
obj_df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>make</th>
      <th>fuel_type</th>
      <th>aspiration</th>
      <th>num_doors</th>
      <th>body_style</th>
      <th>drive_wheels</th>
      <th>engine_location</th>
      <th>engine_type</th>
      <th>num_cylinders</th>
      <th>fuel_system</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>convertible</td>
      <td>rwd</td>
      <td>front</td>
      <td>dohc</td>
      <td>four</td>
      <td>mpfi</td>
    </tr>
    <tr>
      <th>1</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>convertible</td>
      <td>rwd</td>
      <td>front</td>
      <td>dohc</td>
      <td>four</td>
      <td>mpfi</td>
    </tr>
    <tr>
      <th>2</th>
      <td>alfa-romero</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>hatchback</td>
      <td>rwd</td>
      <td>front</td>
      <td>ohcv</td>
      <td>six</td>
      <td>mpfi</td>
    </tr>
    <tr>
      <th>3</th>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>four</td>
      <td>sedan</td>
      <td>fwd</td>
      <td>front</td>
      <td>ohc</td>
      <td>four</td>
      <td>mpfi</td>
    </tr>
    <tr>
      <th>4</th>
      <td>audi</td>
      <td>gas</td>
      <td>std</td>
      <td>four</td>
      <td>sedan</td>
      <td>4wd</td>
      <td>front</td>
      <td>ohc</td>
      <td>five</td>
      <td>mpfi</td>
    </tr>
  </tbody>
</table>
</div>



## Try out the `Backward Difference Encoder` on the engine_type column


```python
encoder = ce.backward_difference.BackwardDifferenceEncoder(cols=["engine_type"])
encoder.fit(obj_df, verbose=1)
```




    BackwardDifferenceEncoder(cols=['engine_type'], drop_invariant=False,
                 handle_unknown='impute', impute_missing=True, return_df=True,
                 verbose=0)




```python
encoder.transform(obj_df).iloc[:,0:7].head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>col_engine_type_0</th>
      <th>col_engine_type_1</th>
      <th>col_engine_type_2</th>
      <th>col_engine_type_3</th>
      <th>col_engine_type_4</th>
      <th>col_engine_type_5</th>
      <th>col_engine_type_6</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>-0.857143</td>
      <td>-0.714286</td>
      <td>-0.571429</td>
      <td>-0.428571</td>
      <td>-0.285714</td>
      <td>-0.142857</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>-0.857143</td>
      <td>-0.714286</td>
      <td>-0.571429</td>
      <td>-0.428571</td>
      <td>-0.285714</td>
      <td>-0.142857</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>0.142857</td>
      <td>-0.714286</td>
      <td>-0.571429</td>
      <td>-0.428571</td>
      <td>-0.285714</td>
      <td>-0.142857</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>0.142857</td>
      <td>0.285714</td>
      <td>-0.571429</td>
      <td>-0.428571</td>
      <td>-0.285714</td>
      <td>-0.142857</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>0.142857</td>
      <td>0.285714</td>
      <td>-0.571429</td>
      <td>-0.428571</td>
      <td>-0.285714</td>
      <td>-0.142857</td>
    </tr>
  </tbody>
</table>
</div>



## Another approach is to use a polynomial encoding.


```python
encoder = ce.polynomial.PolynomialEncoder(cols=["engine_type"])
encoder.fit(obj_df, verbose=1)
```




    PolynomialEncoder(cols=['engine_type'], drop_invariant=False,
             handle_unknown='impute', impute_missing=True, return_df=True,
             verbose=0)




```python
encoder.transform(obj_df).iloc[:,0:7].head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>col_engine_type_0</th>
      <th>col_engine_type_1</th>
      <th>col_engine_type_2</th>
      <th>col_engine_type_3</th>
      <th>col_engine_type_4</th>
      <th>col_engine_type_5</th>
      <th>col_engine_type_6</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>-0.566947</td>
      <td>0.545545</td>
      <td>-0.408248</td>
      <td>0.241747</td>
      <td>-0.109109</td>
      <td>0.032898</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>-0.566947</td>
      <td>0.545545</td>
      <td>-0.408248</td>
      <td>0.241747</td>
      <td>-0.109109</td>
      <td>0.032898</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>-0.377964</td>
      <td>0.000000</td>
      <td>0.408248</td>
      <td>-0.564076</td>
      <td>0.436436</td>
      <td>-0.197386</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>-0.188982</td>
      <td>-0.327327</td>
      <td>0.408248</td>
      <td>0.080582</td>
      <td>-0.545545</td>
      <td>0.493464</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>-0.188982</td>
      <td>-0.327327</td>
      <td>0.408248</td>
      <td>0.080582</td>
      <td>-0.545545</td>
      <td>0.493464</td>
    </tr>
  </tbody>
</table>
</div>


