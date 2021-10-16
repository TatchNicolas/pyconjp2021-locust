# PyCon JP 2021 Locust実践編: Pythonで書く負荷試験一問一答 / Locust in practice: questions and answers for writing load testing in Python

下記で発表した内容のサンプルコード置き場です。 / Sample codes for the following talk.

https://2021.pycon.jp/time-table/?id=269708

## How to run the sample

```sh
kind create cluster --config ./kind.yaml
```

### kubectlで動かす / Run with kubectl

```sh
kubectl apply -f manifests/
```

### kindで動かす / Run with kind

```sh
skaffold run
```
