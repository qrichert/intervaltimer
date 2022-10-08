# Interval Timer

Run callback at given interval, accounting for drift.

`time.sleep()` in a loop constantly accumulates small delays (code
execution time, system delays, etc.), amounting to larger delays over
time (drift). `IntervalTimer` does not, because it corrects drift
continuously.

```python
timer = IntervalTimer(1, lambda: print(time.time()))

print("Run for 10s...")
timer.start_threaded()
time.sleep(10)
timer.stop()
print("Done.")
```

```console
$ python3.10 intervaltimer.py
Run for 10s...
1665220714.435169
1665220715.4377038
1665220716.438622
1665220717.435797
1665220718.439798
1665220719.436366
1665220720.438207
1665220721.4403992
1665220722.435918
1665220723.440477
1665220724.438723
Done.
```
