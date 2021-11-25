# Mealkit_Recommendation
쿠글 4기 밀키트 추천 시스템

마켓컬리와 이마트몰에서 크롤링한 밀키트 정보, 리뷰 데이터를 이용해 유저에게 밀키트 상품을 추천하는 모델입니다.

(이마트몰의 데이터 특성이 너무 달라 마켓컬리로만 최종 진행했습니다.)

### 1. 데이터 수집

selenium을 이용해서 상품정보 데이터와 리뷰 데이터 따로 json 파일로 저장했습니다.

📄 **데이터 파일**
```
— [마켓컬리정보.json](https://github.com/Haebuk/Mealkit_Recommendation/blob/main/data/%EB%A7%88%EC%BC%93%EC%BB%AC%EB%A6%AC%EC%A0%95%EB%B3%B4.json)

— [마켓컬리리뷰.json](https://github.com/Haebuk/Mealkit_Recommendation/blob/main/data/%EB%A7%88%EC%BC%93%EC%BB%AC%EB%A6%AC%EB%A6%AC%EB%B7%B0.json)

— [이마트몰정보.json](https://github.com/Haebuk/Mealkit_Recommendation/blob/main/data/%EC%9D%B4%EB%A7%88%ED%8A%B8%EB%AA%B0%EC%A0%95%EB%B3%B4.json)

— [이마트몰리뷰.json](https://github.com/Haebuk/Mealkit_Recommendation/blob/main/data/%EC%9D%B4%EB%A7%88%ED%8A%B8%EB%AA%B0%EB%A6%AC%EB%B7%B0.json)
```

📋 **데이터 세부 내용**

1. 상품 정보 데이터
    - name : 상품명
    - storeName : 판매처
    - category : 카테고리(한식, 일식_아시안, 중식, 웨스턴)
    - brand : 상품 브랜드
    - price : 가격
    - thumbnailUrl : 상품 이미지 Url
    - contentUrl: 상품 구매 페이지 Url
    - isSoldOut : 매진 여부
    - detail : 상품 설명
2. 리뷰 데이터
    - name : 상품명
    - reviews
        - user : 상품 이용자
        - star : 별점
        - content : 리뷰 내용

** 마켓컬리는 카테고리와 별점 정보가 없어 카테고리는 직접 입력했고, 별점은 감성분석 모델을 이용해 부정, 긍정을 0과 1로 입력했습니다. 

### 2. 데이터 전처리

수집한 데이터 중 사용자명, 브랜드, 카테고리를 각각 one-hot encoding하여 DeepFM의 input으로 사용하였습니다.

### 3. 마켓컬리 리뷰 데이터 감성분석 모델

리뷰의 별점을 추천 모델의 y값으로 사용하려 했으나, 수집한 마켓컬리 데이터에는 별점이 없었습니다.

따라서 리뷰의 긍정/부정을 y로 사용하기 위해 감성분석 모델을 적용하였습니다. 

리뷰 데이터에 구어체가 많기 때문에 네이버 뉴스에서 댓글과 대댓글을 수집하여 구어체 학습에 효과적인 **KcELECTRA 모델**을 사용하였고,  하이퍼 파라미터 튜닝을 통해 Accuracy를 91.71에서 **92.03**까지 높였습니다.

 Accuracy: 0.9203, Loss: 0.2172

[사용한 Pre-trained KcELECTRA 주소](https://github.com/Beomi/KcELECTRA)

### 4. 추천 모델 - DeepFM + Extracted Contents Based Filtering

먼저 Title(상품명)과 Description(상품설명)은 768차원으로 임베딩한 데이터에 Convolution Block을 적용하여 Feature Extraction을 진행했습니다. 

User(사용자)와 Brand, Category는 Sparse Data로 변환해 임베딩 후 deepFM을 수행했습니다.

그리고 각각의 결과를 concat해서 sigmoid에 적용시켜 결과를 얻었습니다.

deepFM에 대한 자세한 내용은 해당 [논문](https://paperswithcode.com/paper/deepfm-an-end-to-end-wide-deep-learning)에서 확인하실 수 있습니다.

- 사용 구조

![image](https://user-images.githubusercontent.com/68543150/143440088-91087b60-9f13-4c54-92ba-5f3080170e6b.png)


- Convolution Block : CNN으로 768차원으로 Embedding된 Title과 Description 데이터에 필터사이즈가 768인 Convolution 필터를 적용시켜 피쳐 추출을 진행했습니다.

- DNN : deepFM의 deep component로, layer는 256 → 64 → 2로 진행했습니다. 그리고 layer마다 Batch Normalization을 적용시켰고, 활성화 함수로는 ReLU를 이용했으며, Dropout도 적용시켰습니다.

 위 모델을 Epoch = 100으로, Optimizer는 Adam을 이용해 학습시켰습니다.  (Early Stopping은 val_auc를 기준으로 patience 5)


### 5. 실험 과정 및 결과

### 6. 추천 결과

 실제로 마켓컬리 모델에 사용자를 입력했을 때 나오는 추천 결과입니다.

— User : 유 *

| 리뷰한 상품 | 추천 상품 |
| --- | --- |
| [르블란서] 돈마호크 스테이크&머스터드 소스 세트 | [My little recipe] 안동에서 올라온 전통찜닭 (2인용) |
| [르블란서] 항정살 스테이크&머스터드 소스 세트 | [Kurly's] 간편하게 바삭, 유린기 |
| [소중한식사] 파래 곤약 비빔면 키트 | [KART] 맛있는 한 판 언양식 불고기 |
| [창화루] 마라 감바스 | [교촌] 리얼 닭강정 핫스파이시 520g |
| [일품식탁] 야채 꼬마김밥세트 | [프롬셰프] 바로 에그인헬 |
|  | [코빅] 시즈닝 아스파라거스 부채살 스테이크 250g(냉장) |
|  | [신사동 가을백반] 우렁 묵은지 쌈밥 키트 |
|  | [레디잇] 닭가슴살 얌운센 |
|  | [도리깨침] 월남쌈 |
|  | [My little recipe] 안동에서 올라온 매콤치즈찜닭 (2인용) |
|  | [해밀 : 바다가 주는 식사] 제철 맞은 가리비 토마토 스튜 581g (리뉴얼) |
|  | [해밀 : 바다가 주는 식사] 홍합&가리비&새우 토마토 스튜 621g (리뉴얼) |
|  | [풍요한 아침] 화이트 오믈렛 100g |
|  | [해밀 : 바다가 주는 식사] 제철 맞은 가리비 로제 스튜 540g |
|  | [모노키친] 차슈 |
|  | [프롬셰프] 바로 라따뚜이 라자냐 |
|  | [벤탄마켓] 감바스 알 아히요 |
|  |  부산 조방낙지 낙곱새 (2인분) |
