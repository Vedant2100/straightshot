
import sys, io, json, time, traceback
_res = {"setup": None, "tests": [], "stdout": "", "viz": None}
_ns = {"__name__": "__main__"}
_buf = io.StringIO(); _old = sys.stdout; sys.stdout = _buf
try:
    exec(compile(USER, "solution.py", "exec"), _ns)
except BaseException:
    _res["setup"] = traceback.format_exc()[-1500:]
for _t in json.loads(TESTS_JSON):
    _t0 = time.perf_counter()
    if _res["setup"]:
        _res["tests"].append({"name": _t["name"], "ok": False, "err": "Your code didn't run (see the error above).", "ms": 0}); continue
    try:
        exec(compile(_t["code"], "test", "exec"), dict(_ns))
        _res["tests"].append({"name": _t["name"], "ok": True, "err": "", "ms": round((time.perf_counter() - _t0) * 1000, 1)})
    except AssertionError as e:
        _res["tests"].append({"name": _t["name"], "ok": False, "err": "AssertionError: " + (str(e) or "assert failed"), "ms": round((time.perf_counter() - _t0) * 1000, 1)})
    except BaseException as e:
        _tb = traceback.format_exc().strip().splitlines()
        _res["tests"].append({"name": _t["name"], "ok": False, "err": "\n".join(_tb[-3:])[-700:], "ms": round((time.perf_counter() - _t0) * 1000, 1)})
if VIZ and not _res["setup"]:
    try:
        import matplotlib; matplotlib.use("AGG")
        import matplotlib.pyplot as plt, base64
        plt.close("all"); exec(compile(VIZ, "viz", "exec"), dict(_ns))
        _f = plt.gcf(); _f.set_size_inches(7.5, 3.6); _f.tight_layout()
        _b = io.BytesIO(); _f.savefig(_b, format="png", dpi=110); _res["viz"] = base64.b64encode(_b.getvalue()).decode()
    except BaseException as e:
        _res["vizErr"] = type(e).__name__ + ": " + str(e)[:300]
sys.stdout = _old
_res["stdout"] = _buf.getvalue()[-4000:]
json.dumps(_res)
