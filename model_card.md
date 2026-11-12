# VibeFinder: Music Recommender Model Card

## 1. Goal / Task

VibeFinder ranks songs by how closely their labels and energy match a user's
preferences. It returns the top requested songs with short explanations.

## 2. Data Used

The catalog has 18 example songs. Each has a genre, mood, energy, tempo,
valence, danceability, and acousticness, along with title and artist.
Recommendations currently use only genre, mood, and energy. The catalog is
small and uneven: lofi appears three times, pop twice, and most other genres
once. Many styles, songs, and listener perspectives are missing.

## 3. Algorithm Summary

An exact genre match earns 2 points, an exact mood match earns 1 point, and
energy similarity earns up to 1 point. Energy points decrease as a song's
energy moves farther from the user's target. Genre and mood labels ignore
capitalization and surrounding spaces, but related labels do not get partial
credit. The recommender sorts by total score and returns the top K songs with
the reasons for their scores.

## 4. Observed Behavior / Biases

Genre is weighted more heavily than mood or energy, so a genre match can keep a
song near the top even when its mood differs. For example, Gym Hero can rank
well for a pop profile even when the user does not prefer its intense mood.
Exact label matching may miss songs with related styles. Energy must be a
finite number between 0 and 1; invalid targets or catalog values are rejected.

## 5. Evaluation Process

I ran High-Energy Pop, Chill Lofi, and Deep Intense Rock profiles, plus
conflicting preferences, an invalid energy target, and labels with different
capitalization and extra spaces. I also compared the default weights with an
experiment that halves genre weight and doubles energy weight. Storm Runner
moved above Sunrise City in that experiment because its mood matched and its
energy was closer. Boundary, invalid-input, ranking, and API-consistency tests
also passed in the test suite. These checks show that the logic behaves as
designed; they do not prove that listeners would like the results.

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
- Expand and balance the catalog; use more of its audio features, such as
  danceability or acousticness, when users express those preferences.

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
