# aws-ecs-rds-cicd-access-analytics

AWSコンテナアーキテクチャ（ECS / Fargate / RDS / ALB / CloudFront / ECR）で構築したブログアクセス分析システム。CloudFormationによるIaCとCI/CDパイプラインを実装。

---

## 概要（何を作ったか・目的）

WordPressブログへのアクセス情報を収集し、アクセス数・人気記事ランキングを可視化するアクセス分析システムをAWS上に構築しました。

ブログサイトからJavaScriptでアクセスAPIへリクエストを送り、FastAPIアプリケーションがログを受信。  
Amazon RDS(MySQL)へ保存し、管理画面で以下の情報を確認できます。

- 今日のアクセス数
- 総アクセス数
- 人気記事ランキング

本プロジェクトの目的は以下です：

- ECS / Docker を用いたコンテナ運用の理解
- CloudFormationによるIaC実践
- CodePipeline / CodeBuild によるCI/CD構築
- ALB / CloudFront / VPC を含めた実践的AWS構成の理解
- RDS連携アプリケーション構築

---

## 構成 / アーキテクチャ

![構成図](images/Docker_cicd.png)

---

## 検証時の構成

- リージョン: ap-northeast-1（東京）
- ECS: Fargate
- DB: Amazon RDS for MySQL
- コンテナ: Python 3.11 + FastAPI
- CloudFront: HTTPS強制
- ALB: ECSへのルーティング
- ECR: Dockerイメージ管理

---

## 使用技術

## AWS

- **Amazon ECS (Fargate)**
  - FastAPIコンテナ実行基盤

- **Amazon ECR**
  - Dockerイメージ保存

- **Amazon RDS (MySQL)**
  - アクセスログ保存

- **Application Load Balancer**
  - CloudFrontからの通信をECSへ転送

- **Amazon CloudFront**
  - HTTPS配信 / ALBへのリクエスト中継

- **Amazon VPC**
  - Public / Private Subnet構成

- **AWS CloudFormation**
  - インフラ構成をコード管理（IaC）

- **AWS CodeBuild**
  - Docker build / ECR push 実行

- **AWS CodePipeline**
  - GitHub push をトリガーに自動デプロイ

- **Amazon CloudWatch Logs**
  - ECSログ監視

- **AWS Systems Manager Session Manager**
  - EC2踏み台不要の安全なサーバ接続

---

## アプリケーション

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **Docker**

---

## 設計・その他

- **draw.io**：構成図作成
- **GitHub**：ソースコード管理

---

## CloudFormation構成の説明

CloudFormationテンプレートにより以下を自動構築します。

- VPC
- Public / Private Subnet
- Security Group
- ALB
- ECS Cluster
- Task Definition
- ECS Service
- ECR
- RDS
- CloudFront
- IAM Role
- CloudWatch Logs

---

## デプロイ方法

1. FastAPIソースコード・Dockerfile・buildspec.yml・CloudFormationテンプレートをGitHubへPush
2. CodePipelineが変更を検知
3. CodeBuildでDocker build実施
4. ECRへPush
5. ECSサービス更新
6. CloudFormationでインフラ管理

---

## 実装機能

### アクセスログ保存API

ブログページアクセス時に `/log` へPOSTし、DBへ保存。

### 管理画面

FastAPIのHTMLレスポンスで簡易ダッシュボードを実装。

表示内容：

- 今日のアクセス数
- 総アクセス数
- 人気記事ランキングTOP5

---

## 工夫・学習したポイント

### 1. 実務に近いAWS構成

単一サービス学習ではなく、以下を組み合わせた実践構成を採用しました。

- CloudFront
- ALB
- ECS
- RDS
- CI/CD

### 2. セキュリティ意識

- ECS / RDS を Private Subnet に配置
- ALBのみPublic公開
- Security Groupで通信制御

### 3. Docker + ECS運用

ローカル開発したFastAPIアプリをコンテナ化し、そのまま本番環境へデプロイ可能な構成を実現しました。

### 4. CORS対応

ブログドメインとAPIドメインが異なるため、FastAPI + CloudFront 双方でCORS設定を実施しました。

---

## 開発中に直面した課題と解決策

