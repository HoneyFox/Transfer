using System;
using System.Collections;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System.Linq;
using UnityEngine;

public class MainUpdater : MonoBehaviour
{
    List<Tuple<IList<IUpdate>, uint>> updateList = new List<Tuple<IList<IUpdate>, uint>>();
    Queue<Action> unityActionQueue = new Queue<Action>(256);

    private class TaskInfo
    {
        public IList<IUpdate> taskList;
        public uint phase;
        public Queue<Action> unityActionQueue;
        public int groupIndex;
    }

    List<TaskInfo> taskInfoList = new List<TaskInfo>(64);

    // Start is called before the first frame update
    void Start()
    {
        updateList.Add(new Tuple<IList<IUpdate>, uint>(new List<IUpdate>() { SceneLogic.sInstance }, 0));
        updateList.Add(new Tuple<IList<IUpdate>, uint>(Ball.sBallInstances, 0));
        updateList.Add(new Tuple<IList<IUpdate>, uint>(Ball.sBallInstances, 1));
    }

    // Update is called once per frame
    void Update()
    {
        for(int i = 0; i < updateList.Count; ++i)
        {
            var subList = updateList[i].Item1;
            var phase = updateList[i].Item2;

            for (int j = 0; j < subList.Count; ++j)
            {
                subList[j].PreUpdateSnapshot(phase);
            }

#if PARALLEL_UPDATE
            int taskGroupCount = Mathf.CeilToInt(subList.Count / 20f);
            int maxTaskIndex = subList.Count - 1;

            // Using System.Threading.Tasks.Parallel.For(...)
            /*var result = System.Threading.Tasks.Parallel.For(0, taskGroupCount, (int j) => {
                int taskIndexStart = j * 20;
                for (int k = 0; k < 20; ++k)
                {
                    subList[Mathf.Min(taskIndexStart + k, maxTaskIndex)].OnUpdate(phase, unityActionQueue);
                }
            });
            while (!result.IsCompleted)
                System.Threading.Thread.Sleep(1);
            */

            // Using System.Threading.ThreadPool.QueueUserWorkItem(...)
            _taskCompleted = 0;
            for (int j = 0; j < taskGroupCount; ++j)
            {
                if (taskInfoList.Count <= j)
                    taskInfoList.Add(new TaskInfo());
                taskInfoList[j].taskList = subList;
                taskInfoList[j].phase = phase;
                taskInfoList[j].unityActionQueue = unityActionQueue;
                taskInfoList[j].groupIndex = j;

                System.Threading.ThreadPool.QueueUserWorkItem(DoTaskGroup, taskInfoList[j]);
                //DoTaskGroup(taskInfoList[j]);
            }
            while (_taskCompleted < taskGroupCount)
                System.Threading.Thread.Sleep(1);
#else
            for (int j = 0; j < subList.Count; ++j)
            {
                subList[j].OnUpdate(phase, unityActionQueue);
            }
#endif
            while (unityActionQueue.Count > 0)
            {
                Action action = null;
                action = unityActionQueue.Dequeue();
                action.Invoke();
            }
        }
    }

    int _taskCompleted = 0;

    private void DoTaskGroup(object userData)
    {
        var taskInfo = (TaskInfo)userData;
        int maxTaskIndex = taskInfo.taskList.Count - 1;
        int taskIndexStart = taskInfo.groupIndex * 20;
        for (int k = 0; k < 20; ++k)
        {
            taskInfo.taskList[Mathf.Min(taskIndexStart + k, maxTaskIndex)].OnUpdate(taskInfo.phase, taskInfo.unityActionQueue);
        }
        System.Threading.Interlocked.Increment(ref _taskCompleted);
    }
}
