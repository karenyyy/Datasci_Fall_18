
# coding: utf-8

# In[1]:


# Import necessary modules and define functions
from datascience import *

from urllib.request import urlopen
import re
def read_url(url):
    return re.sub('\\s+', ' ', urlopen(url).read().decode())


# In[2]:


# Read Little Women
little_women_url = 'https://raw.githubusercontent.com/ehmatthes/pcc_prep/master/chapter_10/little_women.txt'
little_women_text = read_url(little_women_url)
little_women_chapters = little_women_text.split('CHAPTER ')[1:]


# In[25]:


# Extract a piece of text
text = little_women_chapters[0]
print(text)


# In[26]:


# Replace double quotes
text = text.replace('"', '')


# In[27]:


# Replace ',', '.', ';', '!', '?'
text = text.replace(',', '')
text = text.replace('.', '')
text = text.replace(';', '')
text = text.replace('!', '')
text = text.replace('?', '')


# In[28]:


print(text)


# In[15]:


# Get the words
words = text.strip().split()


# In[29]:


print(words[:5])
print(len(words))


# In[19]:


# Count frequencies
unique_words = set(words) # Merge repeated words
freqs = []
for w in set(words):
    freqs.append((w, words.count(w)))


# In[20]:


print(freqs[:5])


# In[21]:


# Find the most frequent words
freqs_sorted = sorted(freqs, key=lambda tup: tup[1], reverse=True)


# In[24]:


# Print the most frequent 10 words:
for tup in freqs_sorted[:10]:
    print(tup)


# In[49]:


# Plot the histogram of word frequencies
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

x = np.array([tup[1] for tup in freqs_sorted])
plt.hist(x, bins=range(50))
plt.ylabel('Counts')
plt.xlabel('Word frequency');


# In[48]:


plt.hist(x, bins=range(50), log=True)
plt.ylabel('Log transformed counts')
plt.xlabel('Log transformed word frequency');


# In[ ]:




