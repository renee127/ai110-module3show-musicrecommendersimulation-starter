# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 


The scorer gives an exact genre match 2 points, twice the 1 point for mood and the maximum 1 point for energy, so it may repeatedly favor a user's preferred genre even when another song better matches their mood or energy. Exact label matching gives no genre or mood credit to related labels, which can exclude songs users might still enjoy and may narrow recommendations around the labels they already chose. An earlier out-of-range energy experiment (target 2.0) gave every song zero energy points; the scorer now rejects target or song energy values outside the finite 0.0–1.0 range, including non-numeric and non-finite values. The weight-shift experiment changed rankings, but without listening feedback or user ratings, the results show sensitivity to weights rather than which ranking is more accurate.

---

## 7. Evaluation  

I tested six profiles: High-Energy Pop (pop/intense, energy 0.93), Chill Lofi (lofi/chill, 0.40), Deep Intense Rock (rock/intense, 0.91), Conflicting Metal/Melancholic/High Energy (metal/melancholic, 0.96), an out-of-range Country/Serene profile (country/serene, 2.0), and a case-insensitive Lofi/CHILL profile (0.40). The expected matching songs rose to the top: Gym Hero for High-Energy Pop, Midnight Coding and Library Rain for Chill Lofi, and Storm Runner for Deep Intense Rock. The surprising result was that Gym Hero can still rank high for a profile that does not prefer happy mood: its pop genre earns 2 points and its high energy can add nearly 1, so it can outrank songs that match mood but not genre.

Comparing High-Energy Pop with Deep Intense Rock, Gym Hero and Storm Runner exchange first place because each matches both requested labels and its profile's target energy exactly; the genre/mood labels and energy target together determine the winner. Comparing High-Energy Pop with the conflicting Metal/Melancholic profile, Gym Hero falls from first to third while Voltage Bloom rises to first, because the preferred genre changes from pop to metal and Voltage Bloom's energy exactly matches 0.96; its mood does not match, but genre and energy outweigh that miss. Comparing Chill Lofi with the case-insensitive Lofi/CHILL profile, the top five and scores are identical: capitalization does not change label matches, and the same energy target preserves the ordering.

The out-of-range Country/Serene profile (target energy 2.0) was initially surprising because the earlier scorer assigned zero energy points to every song, leaving genre and mood to decide the ranking; after adding validation, the CLI reports the profile as rejected instead of returning recommendations. Tests confirm that boundary targets 0.0 and 1.0 remain valid. In the weight-shift experiment for High-Energy Pop, Storm Runner moves above Sunrise City when energy weight doubles and genre weight is halved; this is expected because Storm Runner matches the mood and is closer in energy. These checks show that the scorer responds to its inputs as designed, but without listening feedback or ratings they cannot establish that the recommendations are musically accurate.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
