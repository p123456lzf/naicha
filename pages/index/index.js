//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    guanliyuan: false,
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    phone_num: '',
    money: 0,
    hidden: true,
    hidden2: true,
    inputVal: "",
    inputShowed: false,
  },
  //事件处理函数
  inputTyping: function (e) {
    this.setData({
      inputVal: e.detail.value
    });
  },
  navigateToRecords: function () {
    wx.navigateTo({
      url: '../records/records'
    })
  },
  reflash: function () {
    wx.showLoading({
      title: '刷新中',
    })
    const that = this
    wx: wx.request({
      url: 'https://www.ikjmls.cn/user2/' + app.globalData.openid + '/name/' + app.globalData.name,
      success: function (res) {
        var money = res.data.data[0].money
        that.setData({
          money: money,
        })
        wx.hideLoading()
        wx.showToast({
          title: '刷新成功',
        })
      },
      fail: function (res) { },
      complete: function (res) { },
    })

  },
  get_paynum: function () {
    const that = this
    wx: wx.request({
      url: 'https://www.ikjmls.cn/pay_num/' + app.globalData.openid,
      success: function (res) {
        console.log(res)
        var paynum = res.data.pay_num
        that.setData({
          paynum: paynum,
          hidden2: false,
        })
      },
      fail: function (res) { },
      complete: function (res) { },
    })
  },
  confirm: function (e) {
    console.log(e)
    if (this.data.inputVal != '' && this.data.inputVal.length == 11) {
      const that = this
      var phone_num = this.data.inputVal
      wx: wx.request({
        url: 'https://www.ikjmls.cn/user/' + app.globalData.openid + '/phone/' + phone_num,
        success: function (res) {
          that.setData({
            hidden: true,
            phone_num: phone_num,
          })
        },
        fail: function (res) { },
        complete: function (res) { },
      })
    } else {
      wx.showModal({
        title: '请输入正确的手机号!',
        content: '',
        showCancel: false
      })
    }
  },
  confirm2: function (e) {
    this.setData({
      hidden2: true,
    })
  },
  onLoad: function () {
    const that = this
    if (app.globalData.openid == 'oRFFN5StOZOjVbVGeS4zq_Xdsq1g'){
      that.setData({
        guanliyuan: true
      })
    }
    setTimeout(function () {
      wx: wx.request({
        url: 'https://www.ikjmls.cn/user2/' + app.globalData.openid + '/name/' + app.globalData.name,
        success: function (res) {
          if (res.data.ok == 1 && res.data.data.phone_num != '') {
            console.log(res)
            var money = res.data.data[0].money
            var phone_num = res.data.data[0].phone_num
            that.setData({
              money: money,
              phone_num: phone_num,
            })
          }
          else {
            that.setData({
              hidden: false,
            })
          }
        },
        fail: function (res) { },
        complete: function (res) { },
      })
      if (app.globalData.userInfo) {
        that.setData({
          userInfo: app.globalData.userInfo,
          hasUserInfo: true
        })
      } else if (this.data.canIUse) {
        // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
        // 所以此处加入 callback 以防止这种情况
        app.userInfoReadyCallback = res => {
          that.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      } else {
        // 在没有 open-type=getUserInfo 版本的兼容处理
        wx.getUserInfo({
          success: res => {
            app.globalData.userInfo = res.userInfo
            that.setData({
              userInfo: res.userInfo,
              hasUserInfo: true
            })
          }
        })
      }
    }, 1000)

  },
  getUserInfo: function (e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }
})
