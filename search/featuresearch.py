import pandas
import random

class Featuresearch:
    def __init__(self, data = None):
        if self.data is None:
            print("do something here with dummies and mocks")
        else:
            self.data = pandas.read_csv(data, delim_whitespace=True, header=None)
            self.num_features = len(self.data.columns) - 1 #index is off by one
            self.features = set(range(1, self.num_features + 1)) #index is off in the other direction by one
            #played around for a bit and set is the only way (I found) to deal with combinations and avoid permutations


    def forward_selection(self):
        current_features = set()
        not_used_features = self.features.copy() #copies the set
        accuracy = self.dummy_evaluate(current_features)
        print(f"Using no features and random evaluation I get an accuracy of {accuracy:.1f}")
        print("beginning search.")
        best_total_accuracy = accuracy
        best_total_features = set() #initializing empty set here

        while(not_used_features):
            best_accuracy = -1
            best_feature = None

            # Try each unused feature
            for feature in not_used_features:
                candidate_features = current_features | {feature} #either one
                accuracy = self.dummy_evaluate(candidate_features)
                print(f"Using feature(s) {sorted(candidate_features)} accuracy is {accuracy:.1f}%")

                #now comparing for the best one
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_feature = feature

            current_features.add(best_feature)
            not_used_features.remove(best_feature)

            if best_accuracy > best_total_accuracy:
                best_total_accuracy = best_accuracy #take its place as the new champion
                best_total_features = current_features.copy()
            else:
                print("Warning! Accuracy has decreased!")
            #finally
            print(f"Feature set {sorted(current_features)} was best, accuracy is {best_accuracy:.1f}%")
            print(f"\nFinished search!! The best feature subset is {sorted(best_total_features)}, "f"which has an accuracy of {best_total_accuracy:.1f}%")

    def backward_elimination(self):
        # start with all features
        current_features = set(range(1, self.num_features + 1))
        best_accuracy = self.dummy_evaluate(current_features)
        print(f"Using all features and \"random\" evaluation, I get an accuracy of {best_accuracy:.1f}%")
        print("Beginning search.")

        # then iterativly remove features
        while current_features:
            best_subset = None
            best_new_accuracy = -1  # Initialize with a very low value

            # removing each feature
            for feature in current_features:
                test_features = current_features - {feature}  # Remove one feature
                accuracy = self.dummy_evaluate(test_features)
                print(f"Using feature(s) {sorted(test_features)} accuracy is {accuracy:.1f}%")

                # keep track of the best subset and accuracy
                if accuracy > best_new_accuracy:
                    best_new_accuracy = accuracy
                    best_subset = test_features

            # update current features and accuracy
            if best_subset is not None:
                current_features = best_subset
            if best_new_accuracy < best_accuracy:
                print("(Warning, Accuracy has decreased!)")
            best_accuracy = best_new_accuracy

            # output for each iteration
            if current_features:
                print(f"Feature set {sorted(current_features)} was best, accuracy is {best_accuracy:.1f}%\n")

        print(f"Finished search!! The best feature subset is {sorted(current_features)}, "
              f"which has an accuracy of {best_accuracy:.1f}%")

    def dummy_evaluate(self, subset_of_features):
        return random.uniform(10, 90)

