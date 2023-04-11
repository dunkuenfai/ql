module.exports = {
  phone,
  code,
  access_token,
  postSign,
  getTZquestions,
  postDailyquestions,
  postShare,
  getCk,
  msg,
  getCode
};
var crypto = require("crypto-js");
var SHA256 = crypto.SHA256
var hex_md5 = crypto.MD5
let access_token = ""
let phone = ''
let code = ''
let msg = ''
async function getCode(phone) {

  let urlData = (setData().texts).substring(1)
  let url = 'https://safetyinformation.cn/api/admin/mobile/autoRegLoginMsg/' + phone + '?' + urlData
  console.log(url);
  'https://safetyinformation.cn/api/admin/mobile/autoRegLoginMsg/15917100217&NONCE=JlcdkgYYr0FTIMESTAMP=20220707180224&SIGN_TYPE=SHA256&SIGN=73938ed53a376bd9f251c8901a0345e849103343fa15a3a609cf637bf05b7b09'
  'https://safetyinformation.cn/api/admin/mobile/autoRegLoginMsg/15917100217?NONCE=D8cWyYu6MZc&TIMESTAMP=20220707181506&SIGN_TYPE=SHA256&SIGN=e1d37fb222120489dfe5d9f3a63149c5d59525169b60d414d9897ced0e59e75d'
}



async function getCk(phone, code) {
  let url = "https://safetyinformation.cn/api/auth/app/token/sms?app=APPSMS@" + phone + "&code=" + code;

  let header1 = {
    "Host": "safetyinformation.cn",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "API-VERSION": "2",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9",
    "Authorization": "Basic aW9zOmlvcw==",
  }

  return new Promise((resolve, reject) => {

    wx.request({
      url: url,
      method: "POST",
      header: header1,
      data: setData().jsons,
      timeout: 5000,
      success(res) {
        console.log("获取CK：" + JSON.stringify(res));
        if (res.data.code == 1) {
          resolve("获取CK错误：" + res.data.msg)
          return
        }
        let data = res.data.access_token
        access_token = data
        console.log(data);
        wx.setStorageSync('locateCK', data)
        resolve("获取CK：" + data)
      },
      fail(res) {
        reject(res)
        console.log(res);
        // reject(res)
      }
    })
  })
}
// 每日签到
async function postSign() {
  let header = {
    "Host": "safetyinformation.cn",
    "Connection": "keep-alive",
    "API-VERSION": "2",
    "Accept": "*/*",
    "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9",
    "Authorization": "Bearer " + access_token,
    "Accept-Encoding": "gzip, deflate, br"
  }
  let url = "https://safetyinformation.cn/api/share/usersign/sign";
  let urlData = setData().jsons;
  return new Promise((resolve, reject) => {
    wx.request({
      url: url,
      method: "POST",
      header: header,
      data: urlData,
      success(res) {
        console.log('签到结果：' + JSON.stringify(res));
        let code = res.data.code
        console.log(code);
        if (code == 1) {
          let msg = res.data.msg
          if (msg == "") {
            resolve("签到错误:CK失效")
          }
          resolve("签到结果:" + res.data.msg)
          return
        }
        let data = res.data.msg
        resolve("签到结果：" + data)
      },
      fail(res) {
        console.log(res);
        reject(res)
      }
    })
  })
}

//每日分享
async function postShare() {
  let header = {
    "Host": "safetyinformation.cn",
    "Connection": "keep-alive",
    "API-VERSION": "2",
    "Accept": "*/*",
    "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9",
    "Authorization": "Bearer " + access_token,
    "Accept-Encoding": "gzip, deflate, br"
  }
  let url = "https://safetyinformation.cn/api/share/userpointstask/completeByType/article_share";
  let urlData = setData().jsons
  return new Promise((resolve, reject) => {
    wx.request({
      url: url,
      method: "POST",
      header: header,
      data: urlData,
      success(res) {
        console.log('分享结果:' + JSON.stringify(res));
        let code = res.data.code
        if (code == 1) {
          resolve("分享结果:分享错误")
          return
        }
        resolve("分享结果:分享完成")
      },
      fail(res) {
        console.log(res);
        reject("分享结果:分享错误，检查网络")
      }
    })
  })
}


async function postTZ(id) {
  let header = {
    "Host": "safetyinformation.cn",
    "Connection": "keep-alive",
    "API-VERSION": "2",
    "Accept": "*/*",
    "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9",
    "Authorization": "Bearer " + access_token,
    "Accept-Encoding": "gzip, deflate, br"
  }
  let url = "https://safetyinformation.cn/api/share/challengeExam/end"
  let urlData = setData().jsons;
  let body = {
    "chaId": id,
    "NONCE": urlData.NONCE,
    "rightQuestionNum": Math.floor(Math.random() * 10 + Math.random() * 100 + 5),
    "SIGN_TYPE": "SHA256",
    "TIMESTAMP": urlData.TIMESTAMP,
    "SIGN": urlData.SIGN
  }
  return new Promise((resolve, reject) => {

    wx.request({
      url: url,
      method: "POST",
      header: header,
      data: body,
      success(res) {
        console.log("挑战答题:" + JSON.stringify(res))
        let code = res.data.code
        console.log(code);
        if (code == 1) {
          resolve("挑战答题错误,CK失效")
          return
        }
        resolve("共答对(" + body.rightQuestionNum + "题）")
      },
      fail(res) {
        console.log(res);
        reject("挑战答题错误，检查网络")
      }
    })
  })
  let data = await Api.result(header, body, "POST", url)
  data = data.data
  console.log(data);
  msg = "挑战答题结果：" + JSON.stringify(data)
  return msg

  // let body = {
  //   "chaId": id,
  //   "NONCE": urlData.NONCE,
  //   "rightQuestionNum": Math.random() * 10 + 5,
  //   "SIGN_TYPE": "SHA256",
  //   "TIMESTAMP": urlData.TIMESTAMP,
  //   "SIGN": urlData.SIGN
  // }
  // wx.request({
  //   url: url,
  //   method: "POST",
  //   header: header,
  //   data: body,
  //   success(res) {
  //     let data = res.data
  //     console.log("挑战答题结果：" + JSON.stringify(data)) // 获取签到结果
  //   },
  //   fail(res) {
  //     console.log("连接失败")
  //   }
  // })
}
///**获取挑战答题题目 并提交*/
function getTZquestions() {
  let header = {
    "Host": "safetyinformation.cn",
    "Connection": "keep-alive",
    "API-VERSION": "2",
    "Accept": "*/*",
    "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9",
    "Authorization": "Bearer " + access_token,
    "Accept-Encoding": "gzip, deflate, br"
  }
  let url = "https://safetyinformation.cn/api/share/challengeExam/start?" + setData().texts;
  return new Promise((resolve, reject) => {
    wx.request({
      url: url,
      method: "GET",
      header: header,
      success(res) {
        let id = res.data.data.id
        postTZ(id).then(data => {
          resolve(data)
        }).catch(data => {
          reject("挑战答题结果:挑战答题错误，检查网络")
        })
      },
      fail(res) {
        reject("挑战答题结果:挑战答题错误，检查网络")
        console.log("连接失败")
        wx.showToast({
          title: "连接失败",
          icon: "none"
        })
      }
    })
  })
}

async function postDailyquestions() {
  let header = {
    "Host": "safetyinformation.cn",
    "Connection": "keep-alive",
    "API-VERSION": "2",
    "Accept": "*/*",
    "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9",
    "Authorization": "Bearer " + access_token,
    "Accept-Encoding": "gzip, deflate, br"
  }
  let url = "https://safetyinformation.cn/api/share/user/exam/v2/daily/submit"
  let urlData = setData().jsons;
  let body = {
    "ques": [{
        "userAnswer": [
          "25115378829905"
        ],
        "id": 7705051592210,
        "originOptions": [
          25111994955351,
          25113228547212,
          25115378829905,
          25117650216784
        ]
      },
      {
        "userAnswer": [
          "25182434257475"
        ],
        "id": 7720633838107,
        "originOptions": [
          25176244434964,
          25179180766231,
          25181038477630,
          25182434257475
        ]
      },
      {
        "userAnswer": [
          "25307161599435"
        ],
        "id": 7754553526450,
        "originOptions": [
          25301025856917,
          25303710167472,
          25304283416881,
          25307161599435
        ]
      },
      {
        "userAnswer": [
          "25331027055198"
        ],
        "id": 7759820648701,
        "originOptions": [
          25325932342573,
          25328271786387,
          25331027055198,
          25331745946710
        ]
      },
      {
        "userAnswer": [
          "25342878062834"
        ],
        "id": 7763764455771,
        "originOptions": [
          25342878062834,
          25345369944059,
          25348422072409,
          25350875937996
        ]
      },
      {
        "userAnswer": [
          "25405096193460"
        ],
        "id": 7780838278601,
        "originOptions": [
          25402820878062,
          25405096193460
        ]
      },
      {
        "userAnswer": [
          "25424909495182"
        ],
        "id": 7791339313953,
        "originOptions": [
          25424909495182,
          25426814344148
        ]
      },
      {
        "userAnswer": [
          "27800202918282",
          "27802247437557",
          "27804515683883",
          "27807720024795"
        ],
        "id": 8450910815495,
        "originOptions": [
          27800202918282,
          27802247437557,
          27804515683883,
          27807720024795,
          27808447960056
        ]
      },
      {
        "userAnswer": [
          "27876999047668",
          "27879117867807",
          "27882876657246",
          "27884362568310"
        ],
        "id": 8471118324680,
        "originOptions": [
          27876999047668,
          27879117867807,
          27882876657246,
          27884362568310
        ]
      },
      {
        "userAnswer": [
          "35723101403237",
          "35723688481134",
          "35725828565740"
        ],
        "id": 8476098472467,
        "originOptions": [
          35723101403237,
          35723688481134,
          35725828565740,
          35728185771510
        ]
      }
    ],
    "subType": 2,
    "SIGN_TYPE": "SHA256",
    "TIMESTAMP": urlData.TIMESTAMP,
    "useTimeSeconds": Math.random() * 100,
    "SIGN": urlData.SIGN,
    "startTime": urlData.startTime,
    "NONCE": urlData.NONCE
  }
  return new Promise((resolve, reject) => {
    wx.request({
      url: url,
      method: "POST",
      header: header,
      data: body,
      success(res) {
        console.log("每日答题结果:" + JSON.stringify(res));
        let code = res.data.code
        if (code == 1) {
          resolve("每日答题错误：" + res.data.msg)
          return
        }
        resolve("每日答题结果:每日答题完成")
      },
      fail(res) {
        console.log(res);
        reject("每日答题结果:答题错误，检查网络")
      }
    })
  })
}

function setData() {
  let TIMESTAMP = getTimeStamp()
  var var2 = "";
  let NONCE = getRandomString(11);
  var2 = createSign(NONCE, TIMESTAMP);
  let texts = "&NONCE=" + NONCE + "&SIGN=" + var2 + " & SIGN_TYPE = SHA256&TIMESTAMP = " + TIMESTAMP
  // console.log(var2);
  let jsons = {
    "NONCE": NONCE,
    "TIMESTAMP": TIMESTAMP,
    "SIGN_TYPE": "SHA256",
    "bankIds": ["41", "42"]
  }

  return {
    texts: texts,
    jsons: jsons
  }
}

function createSign(NONCE, TIMESTAMP) {
  let ret = ""; //改成key=value&key=value格式
  let data = NONCE + TIMESTAMP;
  ret = data;
  let md5 = hex_md5(ret);
  ret = "TIMESTAMP=" + TIMESTAMP + "&NONCE=" + NONCE + "&SIGN_TYPE=SHA256&SECRET_KEY=" + md5
  ret = SHA256(ret);
  return ret;
}

function getTimeStamp() {
  let nowDate = new Date()
  let year = nowDate.getFullYear();
  let month = nowDate.getMonth() + 1 < 10 ? "0" + (nowDate.getMonth() + 1) :
    nowDate.getMonth() + 1;
  let day = nowDate.getDate() < 10 ? "0" + nowDate.getDate() : nowDate
    .getDate();
  let HH = nowDate.getHours() < 10 ? "0" + nowDate.getHours() : nowDate
    .getHours();
  let mm = nowDate.getMinutes() < 10 ? "0" + nowDate.getMinutes() : nowDate
    .getMinutes();
  let ss = nowDate.getSeconds() < 10 ? "0" + nowDate.getSeconds() : nowDate
    .getSeconds();
  let TIMESTAMP = year + month + day + HH + mm + ss;
  return TIMESTAMP;
}

function getRandomString(L) {
  let x = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
  let str = ''
  for (let i = 0; i < L; ++i) {
    //重点  这里利用了Math.random()函数生成的随机数大于0 小于1 我们可以
    //用它的随机数来乘以字符串的长度,得到的也是一个随机值，再通过parseInt()
    //函数取整，这样就可以实现字符串的随机取值了
    str += x[parseInt(Math.random() * x.length)]
  }
  return str
}