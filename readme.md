```
const loginResponse = JSON.parse(responseBody);
pm.environment.set("ACCESS_TOKEN", loginResponse.data.access);
```