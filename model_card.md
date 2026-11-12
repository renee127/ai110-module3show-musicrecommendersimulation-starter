# VibeFinder: Music Recommender Model Card

## 1. Goal / Task

VibeFinder ranks songs by how closely their labels and audio-style values match
a user's preferences. It returns the top requested songs with short
explanations.

## 2. Data Used

The catalog has 18 example songs. Each row has genre, mood, energy, tempo,
valence, danceability, acousticness, popularity, release decade, mood tags,
language, and instrumentalness, along with title and artist. The five advanced
attributes and tags are synthetic classroom examples, not verified song
metadata. The catalog is small and uneven: lofi appears three times, pop
twice, and most other genres once. Many styles, songs, and listener
perspectives are missing.

## 3. Algorithm Summary

An exact genre match earns 2 points, an exact mood match earns 1 point, and
energy similarity earns up to 1 point. Energy points decrease as a song's
energy moves farther from the user's target. A user can also choose any of
five optional preferences: popularity similarity, release-decade similarity,
mood-tag overlap, an exact language match, and instrumentalness similarity.
Each enabled preference adds up to 1 point. Genre, mood, tags, and language
ignore capitalization and surrounding spaces. The recommender sorts by total
score and returns the top K songs with the reasons for their scores.

## 4. Observed Behavior / Biases

Genre is weighted more heavily than mood or energy, so a genre match can keep a
song near the top even when its mood differs. For example, Gym Hero can rank
well for a pop profile even when the user does not prefer its intense mood.
Optional preferences can change rankings and profiles with more preferences
can have a higher maximum score. Exact label matching may miss songs with
related styles. The small synthetic catalog cannot establish real listener
preferences. Energy and instrumentalness must be between 0 and 1; invalid
values are rejected.

## 5. Evaluation Process

I ran High-Energy Pop, Chill Lofi, Deep Intense Rock, conflicting, and
case-insensitive label profiles, as well as a profile using all five advanced
preferences. The advanced profile ranked Velvet Groove first because all of
its selected values matched the song's synthetic metadata. I also compared
default weights with an experiment that halves genre weight and doubles energy
weight. Storm Runner moved above Sunrise City in that experiment because its
mood matched and its energy was closer. Boundary, invalid-input, ranking,
loader, and API-consistency tests passed in the test suite. These checks show
that the logic behaves as designed; they do not prove that listeners would
like the results.

Comparing two different profiles shows how the preferences change the list.
High-Energy Pop ranks Gym Hero first (4.00/4), matching pop, intense mood, and
high energy. Chill Lofi ranks Midnight Coding first (3.98/4), matching lofi
and chill with energy close to its lower target; Library Rain is a close
second (3.95/4). Gym Hero does not make the Chill Lofi top five, while the
high-energy songs do not lead that profile. This difference follows from each
profile's genre, mood, and energy preferences, though it does not prove that
real listeners would choose those songs.

## 6. Intended Use and Non-Intended Use

This project is intended for classroom learning and small demonstrations of
content-based recommendations and scoring tradeoffs. It is not intended for
production recommendations or to predict a real person's enjoyment. It has no
listening history, user ratings, or evidence that its labels describe songs
accurately.

## 7. Ideas for Improvement

- Add listener ratings or feedback to evaluate recommendation quality.
- Give partial credit to related genres and moods, and let users adjust
  feature weights.
- Replace synthetic metadata with verified data and expand and balance the
  catalog.

## 8. Personal Reflection

My biggest learning moment was seeing that changing the weights changed the
ranking: genre and mood preferences can outweigh a song's energy match, and
small scoring choices affect what looks like a good recommendation. AI helped
me draft scoring logic, tests, and explanations, but I needed to check the
suggestions against the actual data and run the code because plausible-looking
logic can still produce unexpected results. I was surprised that a simple
combination of a few labels and numbers can feel like a personal
recommendation, even though it does not know what a listener actually enjoys.
Next, I would gather listener ratings, test whether the rankings match those
ratings, and explore partial credit for related genres and moods.

**TODO — Add your own details or revise the draft above:**
- What was your biggest learning moment while building and testing this project?
- How did AI tools help, and what did you need to verify yourself?
- What surprised you about a simple algorithm producing recommendations?
- What would you try next if you continued the project?
