from npm_feature_extractor import NPM_Feature_Extractor


npm_fe = NPM_Feature_Extractor()
input_data = npm_fe.extract_features(r"C:/Users/97091/Desktop/getgithub/npm_download")
print(input_data.head())