import os
import time

IS_ANDROID = False
try:
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread
    IS_ANDROID = True
except Exception as e:
    IS_ANDROID = False

def init_admob():
    if IS_ANDROID:
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            MobileAds = autoclass('com.google.android.gms.ads.MobileAds')
            MobileAds.initialize(PythonActivity.mActivity)
        except Exception as e:
            print(f"[ADMOB INIT ERR] {e}")

def load_and_show_rewarded_ad(on_reward_callback):
    if IS_ANDROID:
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            AdRequest = autoclass('com.google.android.gms.ads.AdRequest$Builder')
            RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
            
            builder = AdRequest()
            ad_request = builder.build()
            test_id = "ca-app-pub-3940256099942544/5224354917"

            class RewardedCallback(PythonJavaClass):
                __javainterfaces__ = ['com/google/android/gms/ads/rewarded/RewardedAdLoadCallback']
                __javacontext__ = 'app'

                def __init__(self, cb):
                    super().__init__()
                    self.cb = cb

                @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
                def onAdLoaded(self, rewarded_ad):
                    class ShowCallback(PythonJavaClass):
                        __javainterfaces__ = ['com/google/android/gms/ads/OnUserEarnedRewardListener']
                        __javacontext__ = 'app'

                        def __init__(self, r_cb):
                            super().__init__()
                            self.r_cb = r_cb

                        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
                        def onUserEarnedReward(self, reward_item):
                            if self.r_cb:
                                self.r_cb()

                    rewarded_ad.show(PythonActivity.mActivity, ShowCallback(self.cb))

                @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
                def onAdFailedToLoad(self, load_error):
                    print(f"[ADMOB LOAD FAIL] {load_error.toString()}")

            RewardedAd.load(PythonActivity.mActivity, test_id, ad_request, RewardedCallback(on_reward_callback))
        except Exception as ex:
            print(f"[ADMOB SHOW EX] {ex}")
            if on_reward_callback:
                on_reward_callback()
    else:
        if on_reward_callback:
            on_reward_callback()
